# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Organization, User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        organization, _ = Organization.objects.get_or_create(name='Organization A')
        instance.organization_id = organization.pk
        instance.save()
        Token.objects.create(user=instance)
