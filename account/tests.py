from django.test import TestCase
from django.urls import reverse
from account.models import Account  # Импортируем кастомную модель
from django.core import mail  # Для тестирования email

class RegisterViewTest(TestCase):
    def test_successful_registration(self):
        """Тест успешной регистрации пользователя"""
        data = {
            "email": "test@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+123456789",
            "fin_code": "ABC1234"
        }
        response = self.client.post(reverse("account:registration"), data)

        # Вывод ошибок формы для отладки
        print(response.context["form"].errors)

        self.assertEqual(Account.objects.count(), 1)  # Проверяем, что пользователь создан

        # Проверяем, что он не активирован (из-за верификации email)
        user = Account.objects.first()
        self.assertFalse(user.is_active)

        # Проверяем, что отправлен email
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Подтверждение адреса электронной почты", mail.outbox[0].subject)

        # Проверяем редирект
        self.assertRedirects(response, reverse("account:login"))

    def test_registration_with_invalid_data(self):
        """Тест регистрации с некорректными данными (пароли не совпадают)"""
        data = {
            "email": "invalid@example.com",
            "password1": "securepassword123",
            "password2": "wrongpassword",
            "first_name": "Invalid",
            "last_name": "User",
            "phone_number": "+987654321",
            "fin_code": "DEF5678"
        }
        response = self.client.post(reverse("account:registration"), data)

        # Проверяем, что пользователь не создан
        self.assertEqual(Account.objects.count(), 0)

        # Проверяем, что остаемся на той же странице (ошибка)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/registration.html")

        # Проверяем, что сообщение об ошибке появилось
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("xəta baş verdi" in str(m) for m in messages))
