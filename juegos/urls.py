from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core (con namespace)
    path("", include("core.urls")),

    # Módulos con namespace propio
    path("lexicon/", include(("lexicon.urls", "lexicon"), namespace="lexicon")),
    path("puzzles/", include(("puzzles.urls", "puzzles"), namespace="puzzles")),
    path("crossword/", include(("crossword.urls", "crossword"), namespace="crossword")),
    path("wordsearch/", include(("wordsearch.urls", "wordsearch"), namespace="wordsearch")),
    path("coloring/", include(("coloring.urls", "coloring"), namespace="coloring")),
    path("calligraphy/", include(("calligraphy.urls", "calligraphy"), namespace="calligraphy")),
    path("sudoku/", include(("sudoku.urls", "sudoku"), namespace="sudoku")),
    path("mandala/", include(("mandala.urls", "mandala"), namespace="mandala")),
    path("maze/", include(("maze.urls", "maze"), namespace="maze")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = "core.views.handler403"
