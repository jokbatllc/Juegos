from django import forms


class ColoringForm(forms.Form):
    TIPO_CHOICES = [("kids", "Niños"), ("adults", "Adultos")]
    TAM_CHOICES = [("A4", "A4"), ("A5", "A5"), ("Carta", "Carta")]
    COM_CHOICES = [
        ("simple", "Simple"),
        ("medio", "Medio"),
        ("detallado", "Detallado"),
    ]

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, initial="kids")
    tamaño = forms.ChoiceField(choices=TAM_CHOICES, initial="A4")
    complejidad = forms.ChoiceField(choices=COM_CHOICES, initial="medio")
    seed = forms.IntegerField(required=False)
    cantidad = forms.IntegerField(min_value=1, max_value=10, initial=1)

    def clean_cantidad(self) -> int:
        cant = self.cleaned_data["cantidad"]
        if cant > 10:
            raise forms.ValidationError("Máximo 10 dibujos")
        return cant

    def to_params(self) -> dict:
        if not self.is_valid():
            raise ValueError("Formulario no válido")
        return self.cleaned_data.copy()
