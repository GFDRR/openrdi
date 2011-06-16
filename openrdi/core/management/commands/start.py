import os
import subprocess

from django.core.management.base import CommandError, NoArgsCommand

class Command(NoArgsCommand):
    can_import_settings = True

    def handle_noargs(self, **options):

        from django.conf import settings
        PROJECT_HOME = os.path.join(settings.PROJECT_ROOT, '..', '..')
        catalina = os.path.join(PROJECT_HOME, 'tomcat', 'bin', 'catalina.sh')

        p = subprocess.Popen([catalina, 'start'])
        pasteini = os.path.join(settings.PROJECT_ROOT, '..', 'extras', 'project.paste.ini')
        p2 = subprocess.Popen(['paster', 'serve', '--reload',  pasteini])
