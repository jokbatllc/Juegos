from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('lexicon/', include('lexicon.urls', namespace='lexicon')),
    path('puzzles/', include('puzzles.urls', namespace='puzzles')),
    path('crossword/', include('crossword.urls', namespace='crossword')),
    path('wordsearch/', include('wordsearch.urls', namespace='wordsearch')),
    path('coloring/', include('coloring.urls', namespace='coloring')),
    path('calligraphy/', include('calligraphy.urls', namespace='calligraphy')),
    path('sudoku/', include('sudoku.urls', namespace='sudoku')),
    path('mandala/', include('mandala.urls', namespace='mandala')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = 'core.views.handler403'
