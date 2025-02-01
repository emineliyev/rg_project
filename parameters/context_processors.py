from .models import Contact


def contact_info(request):
    contact = Contact.objects.first()  # Получаем первый контакт
    return {
        "global_email": contact.email.first().email if contact and contact.email.exists() else None,
        # Передаем строку email
        "global_phone": contact.phone.first().number if contact and contact.phone.exists() else None,
        # Передаем строку phone
        "address": contact.address
    }
