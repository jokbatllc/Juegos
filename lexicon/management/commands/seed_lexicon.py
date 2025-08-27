import json
import random
from collections import deque
from pathlib import Path
from time import perf_counter

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from lexicon.models import Categoria, Idioma, Palabra


class Command(BaseCommand):
    help = "Inserta datos masivos de palabras en la base de datos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--per-lang",
            type=int,
            default=10000,
            help="Número de palabras por idioma",
        )
        parser.add_argument(
            "--langs",
            type=str,
            default="es,en,fr",
            help="Códigos de idioma separados por comas",
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
        parser.add_argument(
            "--dump-json",
            type=str,
            help="Ruta opcional para volcar los datos en JSON/JSONL",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Borra palabras existentes antes de insertar",
        )

    def handle(self, *args, **options):
        per_lang = options["per_lang"]
        batch_size = options["batch_size"]
        langs = [code.strip() for code in options["langs"].split(",") if code.strip()]
        dry_run = options["dry_run"]
        dump_path = options.get("dump_json")
        force = options["force"]

        if dry_run:
            total = per_lang * len(langs)
            self.stdout.write(self.style.NOTICE("Modo dry-run"))
            self.stdout.write(f"Idiomas: {', '.join(langs)}")
            self.stdout.write(f"Se crearían {per_lang} palabras por idioma ({total} en total)")
            if dump_path:
                self.stdout.write(f"Se generaría además un dump en {dump_path}")
            return

        start_total = perf_counter()

        # Fase 1: creación de idiomas y categorías
        t0 = perf_counter()
        lang_defs = {
            "es": "Español",
            "en": "English",
            "fr": "Français",
        }
        lang_objs = {}
        for code in langs:
            name = lang_defs.get(code, code)
            lang_obj, _ = Idioma.objects.get_or_create(
                code=code, defaults={"nombre": name}
            )
            lang_objs[code] = lang_obj

        category_names = [
            "animales",
            "comida",
            "deporte",
            "tecnologia",
            "naturaleza",
            "ciudades",
            "escuela",
            "musica",
            "colores",
            "profesiones",
        ]
        tipo_choices = [
            "wordsearch",
            "crossword",
            "coloring_kids",
            "coloring_adults",
            "calligraphy",
            "sudoku",
            "mandala",
        ]
        categories = []
        for i, name in enumerate(category_names):
            slug = slugify(name)
            tipo = tipo_choices[i % len(tipo_choices)]
            cat, _ = Categoria.objects.get_or_create(
                slug=slug, defaults={"nombre": name, "tipo_contenido": tipo}
            )
            categories.append(cat)
        t1 = perf_counter()
        setup_time = t1 - t0

        total_inserted = {}
        gen_time = 0.0
        insert_time = 0.0
        dump_records = []

        through_model = Palabra.categorias.through

        real_words = {
            "es": deque(
                [
                    "perro",
                    "gato",
                    "manzana",
                    "futbol",
                    "computadora",
                    "bosque",
                    "madrid",
                    "escuela",
                    "guitarra",
                    "rojo",
                ]
            ),
            "en": deque(
                [
                    "dog",
                    "cat",
                    "apple",
                    "soccer",
                    "computer",
                    "forest",
                    "london",
                    "school",
                    "guitar",
                    "red",
                ]
            ),
            "fr": deque(
                [
                    "chien",
                    "chat",
                    "pomme",
                    "football",
                    "ordinateur",
                    "foret",
                    "paris",
                    "ecole",
                    "guitare",
                    "rouge",
                ]
            ),
        }
        synthetic_counters = {code: 1 for code in langs}

        for code in langs:
            lang_obj = lang_objs[code]
            existing = Palabra.objects.filter(idioma=lang_obj).count()
            if existing and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f"{code}: {existing} palabras existentes, omitiendo (use --force para recrear)"
                    )
                )
                total_inserted[code] = 0
                continue
            if existing and force:
                self.stdout.write(f"{code}: eliminando {existing} palabras existentes...")
                Palabra.objects.filter(idioma=lang_obj).delete()

            count_inserted_lang = 0
            words_generated = 0

            while words_generated < per_lang:
                batch_words = []
                batch_cat_links = []
                batch_start_gen = perf_counter()
                for _ in range(min(batch_size, per_lang - words_generated)):
                    cats = random.sample(categories, random.randint(1, 3))
                    prefix = cats[0].slug
                    rw_queue = real_words.get(code)
                    if rw_queue and rw_queue:
                        base = rw_queue.popleft()
                        text = f"{prefix}_{base}".lower()
                    else:
                        idx = synthetic_counters[code]
                        synthetic_counters[code] += 1
                        text = f"{code}_{prefix}_{idx:06d}"
                    difficulty = random.randint(1, 5)
                    tags = None
                    if random.random() < 0.3:
                        tags = {"tema": prefix}
                    word = Palabra(texto=text, idioma=lang_obj, dificultad=difficulty, tags=tags)
                    batch_words.append((word, cats))
                batch_gen_time = perf_counter() - batch_start_gen
                gen_time += batch_gen_time

                batch_start_insert = perf_counter()
                created_words = Palabra.objects.bulk_create(
                    [bw[0] for bw in batch_words], batch_size=batch_size
                )
                through_objects = []
                for word_obj, cats in zip(created_words, [bw[1] for bw in batch_words]):
                    for c in cats:
                        through_objects.append(
                            through_model(palabra_id=word_obj.id, categoria_id=c.id)
                        )
                    if dump_path:
                        dump_records.append(
                            {
                                "texto": word_obj.texto,
                                "idioma": code,
                                "dificultad": word_obj.dificultad,
                                "categorias": [c.slug for c in cats],
                                "tags": word_obj.tags,
                            }
                        )
                through_model.objects.bulk_create(through_objects, batch_size=batch_size)
                batch_insert_time = perf_counter() - batch_start_insert
                insert_time += batch_insert_time

                inserted = len(created_words)
                words_generated += inserted
                count_inserted_lang += inserted

            total_inserted[code] = count_inserted_lang

        if dump_path:
            dump_dir = Path(dump_path).parent
            dump_dir.mkdir(parents=True, exist_ok=True)
            if dump_path.endswith(".jsonl"):
                with open(dump_path, "w", encoding="utf-8") as fh:
                    for record in dump_records:
                        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            else:
                with open(dump_path, "w", encoding="utf-8") as fh:
                    json.dump(dump_records, fh, ensure_ascii=False)
            self.stdout.write(self.style.SUCCESS(f"Dump guardado en {dump_path}"))

        total_time = perf_counter() - start_total

        self.stdout.write("Resumen de inserciones:")
        for code, count in total_inserted.items():
            self.stdout.write(f"  {code}: {count}")
        self.stdout.write(f"Total: {sum(total_inserted.values())}")
        self.stdout.write("Tiempos:")
        self.stdout.write(f"  setup: {setup_time:.2f}s")
        self.stdout.write(f"  generar: {gen_time:.2f}s")
        self.stdout.write(f"  insertar: {insert_time:.2f}s")
        self.stdout.write(f"  total: {total_time:.2f}s")
<<<<<<< ours

=======
>>>>>>> theirs
