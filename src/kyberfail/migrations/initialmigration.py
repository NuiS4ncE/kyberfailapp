from django.db import migrations, models
import datetime, os

def create_initial_user(apps, schema_editor):
    Account = apps.get_model('kyberfail', 'Account')
    User = apps.get_model('auth', 'User')

    user = User.objects.create_user(
        username = "jim",
        email = "jim@jimson.com",
        password = "jim",
        first_name = "Jim",
        last_name = "Jimson"
    )
    Account.objects.create(
        user = user,
        doctor = False
    )

def create_initial_doctor(apps, schema_editor):
    Account = apps.get_model('kyberfail', 'Account')
    User = apps.get_model('auth', 'User')

    user = User.objects.create_user(
        username = "john",
        email = "john@johnson.com",
        password="john",
        first_name="John",
        last_name="Johnson"
    )
    Account.objects.create(
        user = user,
        doctor = True
    )

def create_admin(apps, schema_editor):
    Account = apps.get_model('kyberfail', 'Account')
    User = apps.get_model('auth', 'User')

    user = User.objects.create_user(
        username = str(os.getenv('ADMIN_USERNAME')),
        email = "admin@admin.com",
        password=str(os.getenv('ADMIN_PASSWORD')),
        first_name="Admin",
        last_name="Admin",
        is_staff = True,
        is_superuser = True
    )
    Account.objects.create(
        user = user,
        doctor = True
    )

def create_second_user(apps, schema_editor):
    Account = apps.get_model('kyberfail', 'Account')
    User = apps.get_model('auth', 'User')

    user = User.objects.create_user(
        username = "bob",
        email = "bob@bobson.com",
        password = "bob",
        first_name = "Bob",
        last_name = "Bobson"
    )
    Account.objects.create(
        user = user,
        doctor = False
    )

def create_initial_note(apps, schema_editor):
    Note = apps.get_model('kyberfail', 'Note')
    Account = apps.get_model('kyberfail', 'Account')

    account = Account.objects.get(user__username="jim")

    Note.objects.create(
        title="Flu",
        description="You have a flu my guy",
        createdAt=datetime.datetime.now(),
        user=account.user
    )
    Note.objects.create(
        title="Another flu!",
        description="You did it again!",
        createdAt=datetime.datetime.now(),
        user=account.user
    )

def create_second_note(apps, schema_editor):
    Note = apps.get_model('kyberfail', 'Note')
    Account = apps.get_model('kyberfail', 'Account')

    account = Account.objects.get(user__username="bob")

    Note.objects.create(
        title="Back pain",
        description="You're an old man",
        createdAt=datetime.datetime.now(),
        user=account.user
    )

class Migration(migrations.Migration):

    dependencies = [
        ('kyberfail', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_user),
        migrations.RunPython(create_initial_doctor),
        migrations.RunPython(create_admin),
        migrations.RunPython(create_second_user),
        migrations.RunPython(create_second_note),
        migrations.RunPython(create_initial_note),
    ]
