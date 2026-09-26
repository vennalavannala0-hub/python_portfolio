from django.core.management.base import BaseCommand

from portfolio.seed import seed_portfolio


class Command(BaseCommand):
    help = "Load placeholder portfolio content. Safe to run more than once."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing portfolio content before seeding.",
        )

    def handle(self, *args, **options):
        seed_portfolio(replace_existing=options["replace"])
        self.stdout.write(self.style.SUCCESS("Portfolio content is ready."))
