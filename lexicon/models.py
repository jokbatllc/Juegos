from django.db import models


class Idioma(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class Categoria(models.Model):
    TIPO_CHOICES = [
        ("crossword", "Crossword"),
        ("wordsearch", "Wordsearch"),
        ("coloring_kids", "Coloring Kids"),
        ("coloring_adults", "Coloring Adults"),
        ("calligraphy", "Calligraphy"),
        ("sudoku", "Sudoku"),
        ("mandala", "Mandala"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    tipo_contenido = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.nombre


class Palabra(models.Model):
    texto = models.CharField(max_length=255)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    dificultad = models.PositiveSmallIntegerField(default=1)
    tags = models.JSONField(null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, related_name="palabras", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["texto", "idioma"], name="unique_texto_idioma"
            ),
        ]
        indexes = [
            models.Index(fields=["texto", "idioma"]),
        ]

    def __str__(self) -> str:
        return self.texto


class ListaPalabras(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, related_name="listas", blank=True)
    palabras = models.ManyToManyField(Palabra, related_name="listas", blank=True)

    def __str__(self) -> str:
        return self.nombre


class Word(models.Model):
    LANG_CHOICES = [
        ("es", "Spanish"),
        ("en", "English"),
        ("fr", "French"),
        ("de", "German"),
    ]

    word = models.CharField(max_length=255, unique=True, db_index=True)
    language = models.CharField(max_length=2, choices=LANG_CHOICES)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.word
