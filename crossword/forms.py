from django import forms
from lexicon.models import Idioma, Categoria


class CrosswordForm(forms.Form):
    idioma = forms.ModelChoiceField(queryset=Idioma.objects.all(), required=True)
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(), required=False
    )

    ancho = forms.IntegerField(min_value=5, max_value=20, initial=12)
    alto = forms.IntegerField(min_value=5, max_value=20, initial=12)
    num_palabras = forms.IntegerField(min_value=3, max_value=50, initial=15)
    dificultad_min = forms.IntegerField(min_value=1, max_value=5, initial=1)
    dificultad_max = forms.IntegerField(min_value=1, max_value=5, initial=5)
    seed = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilo Bootstrap por defecto
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned = super().clean()
        ancho = cleaned.get("ancho") or 0
        alto = cleaned.get("alto") or 0
        num_palabras = cleaned.get("num_palabras") or 0

        # No permitir demasiadas palabras para el tamaño del tablero
        if num_palabras > (ancho * alto) // 3:
            self.add_error(
                "num_palabras",
                "Demasiadas palabras para el tamaño del tablero.",
            )

        min_d = cleaned.get("dificultad_min")
        max_d = cleaned.get("dificultad_max")
        if min_d is not None and max_d is not None and min_d > max_d:
            self.add_error(
                "dificultad_max",
                "La dificultad máxima debe ser mayor o igual a la mínima.",
            )

        return cleaned

    def to_params(self):
        data = self.cleaned_data
        # Si no selecciona categorías, usar TODAS
        categorias = (
            [c.id for c in data["categorias"]]
            if data.get("categorias")
            else list(Categoria.objects.values_list("id", flat=True))
        )

        return {
            "idioma": getattr(data["idioma"], "code", data["idioma"]),
            "categorias": categorias,
            "ancho": data["ancho"],
            "alto": data["alto"],
            "num_palabras": data["num_palabras"],
            "dificultad_min": data["dificultad_min"],
            "dificultad_max": data["dificultad_max"],
            "seed": data.get("seed"),
        }
