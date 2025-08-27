from django import forms

SHAPES = [("rect", "Rectangular"), ("circ", "Circular"), ("tri", "Triangular")]
DIFF = [("easy", "Fácil"), ("med", "Media"), ("hard", "Difícil")]


class MazeForm(forms.Form):
    shape = forms.ChoiceField(choices=SHAPES, label="Forma")
    width = forms.IntegerField(
        min_value=5, max_value=200, initial=31, label="Ancho (rect)"
    )
    height = forms.IntegerField(
        min_value=5, max_value=200, initial=31, label="Alto (rect)"
    )
    rings = forms.IntegerField(
        min_value=2, max_value=100, initial=12, required=False, label="Anillos (circ)"
    )
    sectors = forms.IntegerField(
        min_value=4, max_value=360, initial=36, required=False, label="Sectores (circ)"
    )
    tri_size = forms.IntegerField(
        min_value=5, max_value=200, initial=40, required=False, label="Tamaño (tri)"
    )
    difficulty = forms.ChoiceField(choices=DIFF, initial="med", label="Dificultad")
    seed = forms.CharField(required=False, label="Semilla")
