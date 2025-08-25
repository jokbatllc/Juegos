from django.db import models
from django.conf import settings

TIPO_CHOICES = [
    ("crossword", "Crossword"),
    ("wordsearch", "Wordsearch"),
    ("coloring_kids", "Coloring Kids"),
    ("coloring_adults", "Coloring Adults"),
    ("calligraphy", "Calligraphy"),
    ("sudoku", "Sudoku"),
    ("mandala", "Mandala"),
]


class PlantillaJuego(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=255)
    parametros_schema = models.JSONField()

    def __str__(self) -> str:
        return self.nombre


class JuegoGenerado(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    parametros = models.JSONField()
    resultado = models.JSONField(null=True, blank=True)
    seed = models.IntegerField(default=0)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.tipo} #{self.pk}"


class Exportacion(models.Model):
    FORMATO_CHOICES = [
        ("pdf", "PDF"),
        ("png", "PNG"),
        ("svg", "SVG"),
        ("zip", "ZIP"),
    ]
    juego = models.ForeignKey(JuegoGenerado, on_delete=models.CASCADE, related_name="exportaciones")
    formato = models.CharField(max_length=3, choices=FORMATO_CHOICES)
    archivo = models.FileField(upload_to="exports/%Y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.formato} export for {self.juego_id}"
