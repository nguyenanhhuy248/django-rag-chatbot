from __future__ import annotations

from django.db import migrations


def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')

    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


def reverse_user_profiles(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    UserProfile.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_profiles, reverse_user_profiles),
    ]
