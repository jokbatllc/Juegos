import json
from pathlib import Path

from django.core.management.base import BaseCommand

from lexicon.models import Categoria, Idioma, Palabra


class Command(BaseCommand):
    help = "Carga palabras desde un archivo JSON o JSONL"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="lexicon/fixtures/lexicon_seed.json",
            help="Ruta del archivo JSON/JSONL a cargar",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Tamaño de lote para bulk_create",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="No inserta datos, solo muestra lo que haría",
        )

    def handle(self, *args, **options):
        path = Path(options["path"])
        batch_size = options["batch_size"]
        dry_run = options["dry_run"]

        if not path.exists():
            self.stderr.write(self.style.ERROR(f"Archivo {path} no encontrado"))
            return

        def iter_records():
            if path.suffix == ".jsonl":
                with open(path, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if line:
                            yield json.loads(line)
            else:
                with open(path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    for item in data:
                        yield item

        existing_pairs = set(
            Palabra.objects.values_list("texto", "idioma__code")
        )
        languages = {}
        categories = {}
        through_model = Palabra.categorias.through
        batch = []
        inserted = 0

        for rec in iter_records():
            texto = rec.get("texto", "").strip().lower()
            code = rec.get("idioma")
            if not texto or not code:
                continue
            if (texto, code) in existing_pairs:
                continue
            lang = languages.get(code)
            if not lang:
                lang, _ = Idioma.objects.get_or_create(
                    code=code, defaults={"nombre": code}
                )
                languages[code] = lang
            cat_objs = []
            for slug in rec.get("categorias", []):
                cat = categories.get(slug)
                if not cat:
                    cat, _ = Categoria.objects.get_or_create(
                        slug=slug,
                        defaults={
                            "nombre": slug,
                            "tipo_contenido": "wordsearch",
                        },
                    )
                    categories[slug] = cat
                cat_objs.append(cat)
            word = Palabra(
                texto=texto,
                idioma=lang,
                dificultad=rec.get("dificultad", 1),
                tags=rec.get("tags"),
            )
            batch.append((word, cat_objs))
            existing_pairs.add((texto, code))
            if len(batch) >= batch_size:
                if not dry_run:
                    self._flush(batch, batch_size, through_model)
                inserted += len(batch)
                batch = []

        if batch:
            if not dry_run:
                self._flush(batch, batch_size, through_model)
            inserted += len(batch)

        action = "Procesarían" if dry_run else "Insertadas"
        self.stdout.write(
            self.style.SUCCESS(f"{action} {inserted} palabras desde {path}")
        )

    def _flush(self, batch, batch_size, through_model):
        created_words = Palabra.objects.bulk_create(
            [w for w, _ in batch], batch_size=batch_size
        )
        relations = []
        for word_obj, (_, cats) in zip(created_words, batch):
            for cat in cats:
                relations.append(
                    through_model(palabra_id=word_obj.id, categoria_id=cat.id)
                )
        through_model.objects.bulk_create(relations, batch_size=batch_size)
