import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = f'./data/{'ingredients.csv'}'
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                status, created = Ingredient.objects.update_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        print('Данные загружены')
