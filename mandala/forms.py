from django import forms


class MandalaForm(forms.Form):
    symmetry = forms.IntegerField(min_value=6, max_value=24, initial=12)
    rings = forms.IntegerField(min_value=4, max_value=12, initial=7)
    complexity = forms.IntegerField(min_value=1, max_value=10, initial=5)
    seed = forms.IntegerField(required=False)

    def to_params(self) -> dict:
        if not self.is_valid():
            raise forms.ValidationError("Formulario no válido")
        return self.cleaned_data.copy()
