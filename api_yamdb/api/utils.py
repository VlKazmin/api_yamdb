import random
import string

from django.core.mail import send_mail


def generate_confirm_code(lenght=6):
    """Генерирует случайный код из 6 цифр."""
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(lenght))
    return code


def send_confirmation_code(email, code):
    """Функция отправки сообщений."""
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {code}"
    from_email = "your_email@example.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
