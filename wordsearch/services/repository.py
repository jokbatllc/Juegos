from lexicon.models import Palabra


def fetch_palabras(idioma_code, categorias_ids, dificultad_min, dificultad_max, limit):
    qs = Palabra.objects.filter(
        idioma_id=idioma_code,
        dificultad__gte=dificultad_min,
        dificultad__lte=dificultad_max,
    )
    if categorias_ids:
        qs = qs.filter(categorias__in=categorias_ids).distinct()
    qs = qs.values_list("texto", flat=True)[: limit * 3]
    return list(qs)
