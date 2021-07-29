#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        user = self.model(
            email=email, is_staff=False, is_active=True, last_login=now,
            date_joined=now, **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_email_validated = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    email = models.EmailField(
        _('email'), max_length=254, unique=True, help_text=_('User email address.'),
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: +999999999. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Profile model
    """
    STATUS_CHOICES = (
        (1, 'active'),
        (2, 'inactive'),
    )

    USER_TYPE = (
        (1, 'common user'),
        (2, 'premium user'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile',
    )

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    user_type = models.IntegerField(choices=USER_TYPE, default=1, db_index=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    publications_numbers = models.PositiveIntegerField(default=0)
    birthdate = models.DateField()

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}"

    def can_access(self):
        return True

    def get_publications(self):
        return self.publications.all()
