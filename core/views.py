from django.shortcuts import render


def home(request):
    games = [
        ("Crossword", "/crossword/"),
        ("Wordsearch", "/wordsearch/"),
        ("Coloring", "/coloring/"),
        ("Calligraphy", "/calligraphy/"),
        ("Sudoku", "/sudoku/"),
        ("Mandala", "/mandala/"),
        ("Lexicon", "/lexicon/"),
        ("Puzzles", "/puzzles/"),
    ]
    return render(request, "core/home.html", {"games": games})
