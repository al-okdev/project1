from django.core.management.base import BaseCommand, CommandError
from viewer.models import Vacancy


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, file, *args, **options):

        vacancies = []
        with open(file, 'r') as f:
            for line in f.readlines():
                exp, price, comp = line.split('# ')
                comp = comp.strip()
                price = int(price)
                comp = eval(comp)
                comp = ", ".join(comp)

                vacancies.append(Vacancy(experiece=exp, price = price, competentions = comp))

        Vacancy.objects.bulk_create(vacancies)

        self.style.SUCCESS('File to DB')