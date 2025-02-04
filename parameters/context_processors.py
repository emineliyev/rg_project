from .models import Contact


def contact_info(request):
    contact = Contact.objects.first()  # Получаем первый контакт
    return {
        "global_email": contact.email.first().email if contact and contact.email.exists() else None,
        "global_phone": contact.phone.first().number if contact and contact.phone.exists() else None,
        "address": contact.address if contact else "Адрес не указан",  # Добавляем проверку
    }
