from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os

SU_NAM = os.getenv('SU_NAM')
SU_PASS = os.getenv('SECRET_KEY')

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username=f"{SU_NAM}").exists():
            User.objects.create_superuser(
                username=f"{SU_NAM}",
                password=f"{SU_PASS}"
            )
        print('Superuser has been created.')