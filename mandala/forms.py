from django import forms


class MandalaForm(forms.Form):
    SIZE_CHOICES = [
        ("A4", "A4"),
        ("A5", "A5"),
        ("500", "500x500px"),
        ("1000", "1000x1000px"),
    ]
    COMPLEXITY_CHOICES = [
        ("simple", "Simple"),
        ("medio", "Medio"),
        ("detallado", "Detallado"),
        ("extremo", "Extremo"),
    ]
    SYM_CHOICES = [("4", "4"), ("6", "6"), ("8", "8"), ("12", "12")]

    tamaño = forms.ChoiceField(choices=SIZE_CHOICES, initial="A4")
    complejidad = forms.ChoiceField(choices=COMPLEXITY_CHOICES, initial="medio")
    simetría = forms.ChoiceField(choices=SYM_CHOICES, initial="6")
    semilla = forms.IntegerField(required=False)
    cantidad = forms.IntegerField(min_value=1, max_value=10, initial=1)

    def clean_cantidad(self) -> int:
        cant = self.cleaned_data["cantidad"]
        if cant > 10:
            raise forms.ValidationError("Máximo 10 mandalas")
        return cant

    def to_params(self) -> dict:
        if not self.is_valid():
            raise ValueError("Formulario no válido")
        return self.cleaned_data.copy()
