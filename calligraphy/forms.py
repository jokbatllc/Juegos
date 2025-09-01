from django import forms
from lexicon.models import Idioma, Categoria


class CalligraphyForm(forms.Form):
    idioma = forms.ModelChoiceField(queryset=Idioma.objects.all(), required=True)
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(), required=False
    )

    fuente = forms.ChoiceField(
        choices=[
            ("manuscrita", "Manuscrita"),
            ("cursiva", "Cursiva"),
            ("mayúsculas", "Mayúsculas"),
            ("mixta", "Mixta"),
        ],
        initial="manuscrita",
    )
    tamaño_letra = forms.TypedChoiceField(
        choices=[(12, "12 pt"), (18, "18 pt"), (24, "24 pt"), (36, "36 pt")],
        coerce=int,
        initial=24,
    )
    num_paginas = forms.IntegerField(min_value=1, max_value=50, initial=5)
    lineado = forms.ChoiceField(
        choices=[
            ("pauta", "Pauta"),
            ("cuadrícula", "Cuadrícula"),
            ("blanco", "Blanco"),
        ],
        initial="pauta",
    )
    contenido = forms.ChoiceField(
        choices=[("letras", "Letras"), ("palabras", "Palabras"), ("frases", "Frases")],
        initial="letras",
    )
    seed = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilos Bootstrap por defecto
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    def clean_num_paginas(self):
        num = self.cleaned_data["num_paginas"]
        if num > 50:
            raise forms.ValidationError("Demasiadas páginas")
        return num

    def to_params(self):
        if not self.is_valid():
            raise ValueError("Formulario no válido")

        data = self.cleaned_data
        # Si no selecciona categorías, usar todas
        categorias = (
            [c.id for c in data.get("categorias", [])]
            if data.get("categorias")
            else list(Categoria.objects.values_list("id", flat=True))
        )

        return {
            "idioma": getattr(data["idioma"], "code", data["idioma"]),
            "categorias": categorias,
            "fuente": data["fuente"],
            "tamaño_letra": data["tamaño_letra"],
            "num_paginas": data["num_paginas"],
            "lineado": data["lineado"],
            "contenido": data["contenido"],
            "seed": data.get("seed"),
        }
