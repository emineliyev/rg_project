# 1. Встроенные библиотеки Python
import secrets

# 2. Django и сторонние библиотеки
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=60, verbose_name='Ad')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ölkə'
        verbose_name_plural = 'Ölkələr'
        ordering = ['name']


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ölkə')
    name = models.CharField(max_length=60, verbose_name='Ad')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Şəhər'
        verbose_name_plural = 'Şəhərlər'
        ordering = ['name']


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        # Отправка письма для подтверждения адреса электронной почты
        user.send_verification_email()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    is_active = models.BooleanField(default=False, verbose_name='Status')
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, verbose_name='Ad')
    last_name = models.CharField(max_length=255, verbose_name='Soyad')
    phone_number = models.CharField(max_length=255, verbose_name='Telefon')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ölkə')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Şəhər')
    address = models.CharField(max_length=255, verbose_name='Ünvan')
    postal_code = models.CharField(max_length=255, verbose_name='Poçt kodu')
    fin_code = models.CharField(max_length=7, unique=True, verbose_name='Fin kod')
    avatar = models.ImageField(upload_to='avatars/Y/d/m/', blank=True, null=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def send_verification_email(self):
        subject = 'Подтверждение адреса электронной почты'
        # Это если реальный проект
        # message = 'Для подтверждения адреса перейдите по ссылке: http://yourdomain.com/verify-email/?token={}'.format(self.generate_verification_token())

        domain = 'http://localhost:8000'
        self.verification_token = self.generate_verification_token()  # Генерация токена
        self.save()  # Сохранение модели, чтобы токен был записан в базу данных
        message = f'Для подтверждения адреса перейдите по ссылке: {domain}/verify-email/?token={self.verification_token}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email])

    def generate_verification_token(self):
        """
        Генерация токена для подтверждения адреса электронной почты
        """
        token_length = 64  # Длина токена, которая точно помещается в max_length=100
        return secrets.token_urlsafe(token_length // 2)


@receiver(pre_save, sender=Account)
def fin_upper(sender, instance, **kwargs):
    instance.fin_code = instance.fin_code.upper()


@receiver(pre_save, sender=Account)
def first_name_adn_last_name_title(sender, instance, **kwargs):
    instance.first_name = instance.first_name.title()
    instance.last_name = instance.last_name.title()
