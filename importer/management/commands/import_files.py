from django.core.management.base import BaseCommand

from importer.services import parse_file, save_records


class Command(BaseCommand):
    help = 'Reads files and imports them into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        records = parse_file(options['file_path'])
        count = save_records(records)
        self.stdout.write(f"Imported {count} records")
