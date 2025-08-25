from django.contrib import admin
from .models import PlantillaJuego, JuegoGenerado, Exportacion


@admin.register(PlantillaJuego)
class PlantillaJuegoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo")
    search_fields = ("nombre",)
    list_filter = ("tipo",)


@admin.register(JuegoGenerado)
class JuegoGeneradoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "seed", "creado_por", "created_at")
    search_fields = ("id",)
    list_filter = ("tipo", "creado_por", "created_at")


@admin.register(Exportacion)
class ExportacionAdmin(admin.ModelAdmin):
    list_display = ("id", "juego", "formato", "archivo", "created_at")
    search_fields = ("juego__id",)
    list_filter = ("formato", "created_at")
