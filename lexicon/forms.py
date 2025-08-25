from __future__ import annotations

import json
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Categoria, Idioma, ListaPalabras, Palabra


class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ["code", "nombre"]

    def clean_code(self):
        code = self.cleaned_data["code"].strip().lower()
        if not (2 <= len(code) <= 5):
            raise ValidationError("El código debe tener entre 2 y 5 caracteres")
        return code


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "slug", "tipo_contenido"]

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if not slug:
            slug = slugify(self.cleaned_data.get("nombre", ""))
        return slug


class PalabraForm(forms.ModelForm):
    class Meta:
        model = Palabra
        fields = ["texto", "idioma", "dificultad", "categorias", "tags"]
        widgets = {"categorias": forms.CheckboxSelectMultiple}

    def clean_texto(self):
        return self.cleaned_data["texto"].strip().lower()

    def clean_tags(self):
        value = self.cleaned_data.get("tags")
        if not value:
            return {}
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValidationError("JSON inválido") from exc


class ListaPalabrasForm(forms.ModelForm):
    class Meta:
        model = ListaPalabras
        fields = ["nombre", "descripcion", "idioma", "categorias", "palabras"]
        widgets = {
            "categorias": forms.CheckboxSelectMultiple,
            "palabras": forms.SelectMultiple,
        }


class ImportCSVForm(forms.Form):
    TIPO_CHOICES = [("palabras", "Palabras"), ("categorias", "Categorías")]

    archivo = forms.FileField()
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
    idioma = forms.ModelChoiceField(queryset=Idioma.objects.all(), required=False)
    columnas = forms.CharField(required=False, help_text="texto,categorias,dificultad,tags")
    separador = forms.CharField(max_length=1, initial=",")
    tiene_encabezados = forms.BooleanField(required=False, initial=True)
