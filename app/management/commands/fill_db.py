from django.core.management import BaseCommand

from app.test_data import TestDataProvider


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("count", nargs="+", type=int)

    def success(self, x, table_name):
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {x} {table_name}')
        )

    def handle(self, *args, **options):
        count = options["count"][0]
        database_provider = TestDataProvider(count)
        database_provider.set_callbacks(
            self.success
        )
        database_provider.fill()

        self.stdout.write(
            self.style.SUCCESS('Successfully filled database')
        )

