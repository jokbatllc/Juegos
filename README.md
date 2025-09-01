# Juegos

  Proyecto Django para generar y exportar **crucigramas**, **sopas de letras**, **sudokus**, **dibujos para colorear**, **cuadernos de caligrafía** y **mandalas**.  
Incluye un **Lexicon** para gestionar palabras y categorías.

---
   Proyecto Django para generar y exportar crucigramas, sopas de letras, sudokus, dibujos para colorear, cuadernos de caligrafía y mandalas. Incluye un Lexicon para gestionar palabras y categorías.
 

## Instalación

1. Crear y activar un entorno virtual:
     ```bash
   python -m venv venv && source venv/bin/activate     # Linux/Mac
   # En Windows:  venv\Scripts\activate
      `python -m venv venv && source venv/bin/activate`
2. Instalar dependencias:
   `pip install -r requirements.txt`
3. Ejecutar migraciones:
   `python manage.py migrate`
4. Generar datos iniciales del léxico:
   `python manage.py seed_lexicon --per-lang 10000 --langs es,en,fr`
   (opcional) cargar desde JSON existente:
   `python manage.py load_lexicon_seed --path lexicon/fixtures/lexicon_seed.json`
5. Crear un superusuario:
   `python manage.py createsuperuser`
6. Iniciar el servidor de desarrollo:
   `python manage.py runserver`

## Datasets

El repositorio solo incluye pequeños archivos de ejemplo en
`lexicon/datasets/*_sample.csv`, utilizados por la batería de tests.

Para generar datasets grandes en local:

```
python scripts/generate_dataset.py --lang es --size 10000
python manage.py import_words --file lexicon/datasets/auto_es_10000.csv
```

Los CSV generados se guardan en `lexicon/datasets/` y están ignorados por
`.gitignore`, por lo que **no deben subirse** al repositorio. Para importar los
datasets de muestra incluidos simplemente ejecuta:

```
python manage.py import_words
```

## Roles y usuarios demo

| Rol               | Puede hacer                                               |
|-------------------|-----------------------------------------------------------|
| editor_contenidos | CRUD y CSV en Lexicon                                    |
| generador         | Crear juegos y exportar                                   |
| visor             | Ver listados/detalles y descargas existentes              |

Configura grupos y usuarios de prueba:

```
python manage.py setup_roles
python manage.py create_demo_users
```

Usuarios disponibles: `editor/editor123`, `maker/maker123`, `viewer/viewer123`.

## Flujo completo

1. Inicia sesión con `maker/maker123`.
2. Ve a `/wordsearch/` y crea una sopa de letras de 10x10.
3. Tras el redirect a `detail/<id>`, revisa la cuadrícula y palabras.
4. Exporta el resultado a PDF y PNG usando los botones correspondientes.
5. Entra a `/admin/` y verifica los registros en **Exportaciones**.

## Otros juegos

- `/crossword/` – crucigramas parametrizables con exportación PDF/PNG.
- `/sudoku/` – sudokus de diversos tamaños y dificultades.
- `/coloring/` – dibujos para colorear para niños o adultos.
- `/calligraphy/` – cuadernos de caligrafía exportables a PDF.
- `/mandala/` – generador de mandalas con exportación a PDF/ZIP.
- `/lexicon/` – CRUD de idiomas, categorías, palabras y listas con importación CSV.

## Calidad

```
make lint    # ruff + isort + black
make test    # pytest -q
```

Para ejecutar todas las pruebas (unitarias e integración):

```
pytest
```

## DX extra

```
pip install pre-commit
pre-commit install
```

Después de instalar los hooks, se ejecutarán automáticamente al hacer commit.

## Docker

1. Copia `.env.example` a `.env` y ajusta las variables necesarias.
2. Desarrollo:
   ```
   docker compose up --build
   ```
   Abre http://localhost:8000
3. Producción local:
   ```
   docker compose -f docker-compose.prod.yml --env-file .env up --build -d
   ```
   Abre http://localhost (Nginx en el puerto 80)
4. Crear superusuario:
   ```
   docker compose exec web python manage.py createsuperuser
   ```
5. Los volúmenes `static_volume` y `media_volume` preservan archivos estáticos y subidos.

En modo producción, Nginx sirve `/static/` y `/media/` directamente y actúa como proxy inverso hacia Gunicorn. La ruta `/health/` responde `ok`.

Para HTTPS puedes considerar soluciones como `nginx-proxy` con `acme-companion`, Caddy o certbot (no implementado aquí).

## Despliegue en VPS

Consulta [docs/deploy/README_VPS.md](docs/deploy/README_VPS.md) para instrucciones paso a paso sobre cómo desplegar el proyecto en un servidor Ubuntu usando Docker Compose, Nginx y systemd.

**Recordatorios de seguridad:**
- Establece `DJANGO_DEBUG=0` en producción.
- Usa una `SECRET_KEY` fuerte y única.
- Configura `ALLOWED_HOSTS` con tu dominio o IP.
- Define credenciales robustas para la base de datos.
- Realiza copias de seguridad periódicas del volumen de Postgres (`db_data`).

## Sopa de letras

Tras generar una sopa de letras, la página de detalle ofrece descargas separadas del tablero, la lista de palabras y la solución en PDF, PNG o TXT. Puedes elegir el fondo blanco o transparente añadiendo `?bg=white` o `?bg=transparent` a la URL de descarga. Al generar varias sopas a la vez se muestran en una lista con enlaces individuales de descarga.
 
