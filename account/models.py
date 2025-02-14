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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
    def create_user(self, email, fin_code, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError(_('Email обязателен'))
        if not fin_code:
            raise ValueError(_('Fin kod обязателен'))

        email = self.normalize_email(email)
        user = self.model(email=email, fin_code=fin_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        user.send_verification_email()  # ✅ Отправка письма после сохранения

        return user

    def create_superuser(self, email, fin_code, password, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, fin_code, password, **extra_fields)


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
        """Отправка письма с подтверждением email"""
        if not self.verification_token:
            self.verification_token = self.generate_verification_token()
            self.save(update_fields=['verification_token'])  # ✅ Обновляем только поле `verification_token`

        subject = 'Подтверждение адреса электронной почты'
        domain = settings.SITE_DOMAIN  # ✅ Теперь домен берется из settings
        verification_link = f'{domain}/verify-email/?token={self.verification_token}'

        # ✅ Рендерим HTML-шаблон письма
        html_message = render_to_string('account/verification_email.html', {'verification_link': verification_link})

        # ✅ Создаем email с HTML и текстовым содержанием
        email = EmailMultiAlternatives(subject, f'Для подтверждения перейдите по ссылке: {verification_link}',
                                       settings.EMAIL_HOST_USER, [self.email])
        email.attach_alternative(html_message, "text/html")

        email.send()

    def generate_verification_token(self):
        """
        Генерация фиксированного 32-символьного токена для подтверждения email
        """
        return secrets.token_hex(16)  # Генерирует ровно 32 символа

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'


@receiver(pre_save, sender=Account)
def fin_upper(sender, instance, **kwargs):
    """Делаем FIN код верхним регистром (если он есть)"""
    if instance.fin_code:
        instance.fin_code = instance.fin_code.upper()


@receiver(pre_save, sender=Account)
def first_name_and_last_name_title(sender, instance, **kwargs):
    """Делаем `first_name` и `last_name` с заглавной буквы (если они есть)"""
    if instance.first_name:
        instance.first_name = instance.first_name.title()
    if instance.last_name:
        instance.last_name = instance.last_name.title()
