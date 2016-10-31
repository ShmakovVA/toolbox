from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.management import create_permissions

modern_django = False

try:
    # django >=1.7
    from django.apps import apps
    modern_django = True
except ImportError:
    # django <1.7
    from django.db.models import get_apps


class Command(NoArgsCommand):
    help = "Add any missing permissions"

    def handle(self, *args, **options):
        if args:
            raise CommandError("Command doesn't accept any arguments")
        return self.handle_noargs(**options)

    def handle_noargs(self, *args, **options):
        if modern_django:
            for app in apps.get_app_configs():
                create_permissions(app, None, options['verbosity'])
        else:
            for app in get_apps():
                create_permissions(app, None, options['verbosity'])
