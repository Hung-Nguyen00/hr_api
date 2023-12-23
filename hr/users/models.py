from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from model_utils.managers import SoftDeletableManagerMixin
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField
from employee.constants import DISPLAY_FIELDS


class CustomUserManager(SoftDeletableManagerMixin, UserManager):
    pass


class Organization(TimeStampedModel):
    name = models.CharField(max_length=100)
    display_fields = ArrayField(
        models.CharField(max_length=50, choices=DISPLAY_FIELDS), blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_removed = models.BooleanField(default=False)

    objects = CustomUserManager()
    available_objects = CustomUserManager()
    all_objects = UserManager()
