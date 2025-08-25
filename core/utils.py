from django.urls import reverse

DETAIL_URLS = {
    "wordsearch": lambda pk: reverse("wordsearch:detail", args=[pk]),
    "crossword": lambda pk: reverse("crossword:detail", args=[pk]),
    "sudoku": lambda pk: reverse("sudoku:detail", args=[pk]),
    "coloring_kids": lambda pk: reverse("coloring:detail", args=[pk]),
    "coloring_adults": lambda pk: reverse("coloring:detail", args=[pk]),
    "calligraphy": lambda pk: reverse("calligraphy:detail", args=[pk]),
    "mandala": lambda pk: reverse("mandala:detail", args=[pk]),
}
