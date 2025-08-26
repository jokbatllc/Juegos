from lexicon.models import Palabra


def fetch_palabras(idioma_code, categorias_ids, dificultad_min, dificultad_max, limit):
    qs = Palabra.objects.filter(
        idioma_id=idioma_code,
        dificultad__gte=dificultad_min,
        dificultad__lte=dificultad_max,
    )
    if categorias_ids:
        qs = qs.filter(categorias__in=categorias_ids).distinct()
    qs = qs.prefetch_related('categorias')[: limit * 3]
    resultados = []
    for p in qs:
        definicion = ', '.join(p.categorias.values_list('nombre', flat=True)) or p.texto
        resultados.append({'texto': p.texto, 'definicion': definicion})
    return resultados
