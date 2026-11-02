import os
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecuestre_project.settings')
import django

django.setup()

from django.template.loader import get_template

bad = []
for f in sorted(glob.glob('templates/**/*.html', recursive=True)):
    rel = f.replace('\\', '/').replace('templates/', '', 1)
    try:
        get_template(rel)
    except Exception as ex:
        bad.append((f, str(ex)))
print('TEMPLATES_ROTOAS:', bad)
