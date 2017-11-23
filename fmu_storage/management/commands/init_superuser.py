from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)


    def handle(self, *args, **options):
        user_name = options['username']
        user_email = "admin@email.com"
        user_passwd = options['password']

        try:
            user = User.objects.get(username = user_name)
            if not user.is_superuser:
                raise Exception("User:%s already exists - and is not super user" % user_name)
            user.set_password(user_passwd)
            user.save()
        except User.DoesNotExist:
            User.objects.create_superuser(user_name, user_email, user_passwd)


