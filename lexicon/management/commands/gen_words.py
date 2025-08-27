import csv
import random
from pathlib import Path

from django.core.management.base import BaseCommand

WORDS = {
    'es': [
        'casa',
        'perro',
        'gato',
        'arbol',
        'nino',
        'coche',
        'playa',
        'montana',
        'rio',
        'sol',
        'luna',
        'flor',
        'libro',
        'pan',
        'vino',
    ]
    * 800,
    'en': [
        'house',
        'dog',
        'cat',
        'tree',
        'child',
        'car',
        'beach',
        'mountain',
        'river',
        'sun',
        'moon',
        'flower',
        'book',
        'bread',
        'wine',
    ]
    * 800,
    'fr': [
        'maison',
        'chien',
        'chat',
        'arbre',
        'enfant',
        'voiture',
        'plage',
        'montagne',
        'riviere',
        'soleil',
        'lune',
        'fleur',
        'livre',
        'pain',
        'vin',
    ]
    * 800,
}


class Command(BaseCommand):
    help = "Genera CSV de 10k palabras por idioma en lexicon/datasets/auto_{lang}_{size}.csv"

    def add_arguments(self, parser):
        parser.add_argument('--langs', default='es,en,fr')
        parser.add_argument('--size', type=int, default=10000)

    def handle(self, *args, **opts):
        langs = opts['langs'].split(',')
        size = opts['size']
        outdir = Path('lexicon/datasets')
        outdir.mkdir(parents=True, exist_ok=True)
        for lang in langs:
            pool = WORDS.get(lang, WORDS['es'])
            data = [random.choice(pool) for _ in range(size)]
            path = outdir / f'auto_{lang}_{size}.csv'
            with path.open('w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['word', 'lang'])
                for wv in data:
                    w.writerow([wv, lang])
            self.stdout.write(self.style.SUCCESS(f'Creado {path}'))
