from __future__ import annotations

import math
from django import forms


class SudokuForm(forms.Form):
    TAM_CHOICES = [(n, f"{n}x{n}") for n in (4, 6, 9, 12, 16)]
    DIF_CHOICES = [
        ("fácil", "Fácil"),
        ("medio", "Medio"),
        ("difícil", "Difícil"),
        ("experto", "Experto"),
    ]

    tamaño = forms.TypedChoiceField(choices=TAM_CHOICES, coerce=int, initial=9)
    dificultad = forms.ChoiceField(choices=DIF_CHOICES, initial="medio")
    seed = forms.IntegerField(required=False)

    def clean_tamaño(self) -> int:
        size = self.cleaned_data["tamaño"]
        root = int(math.sqrt(size))
        if size % root != 0:
            raise forms.ValidationError("Tamaño no soportado")
        return size

    def to_params(self) -> dict:
        if not self.is_valid():
            raise ValueError("Formulario no válido")
        data = self.cleaned_data
        return {"tamaño": data["tamaño"], "dificultad": data["dificultad"], "seed": data.get("seed")}
