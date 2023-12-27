from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):
    # Os campos password, last_login, is_superuser são criados automaticamente do AbstractBaseUser
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    email = models.EmailField(
        unique=True, max_length=100, blank=False, null=False, db_index=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'user'
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser


class CustomGroup(Group):
    class Meta:
        db_table = 'users_groups'
        proxy = True
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'


class CustomPermission(Permission):
    class Meta:
        db_table = 'users_permissions'
        proxy = True
        verbose_name = 'permissão'
        verbose_name_plural = 'permissões'