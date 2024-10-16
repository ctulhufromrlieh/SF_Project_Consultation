from datetime import datetime
from django.core.mail import EmailMultiAlternatives

from .models import  SlotStatusActionType

def send_email_about_new_user(user, group_name, password):
    if group_name=="clients":
        role_caption = "Клиент сервиса"
    elif group_name=="specialists":
        role_caption = "Специалист"
    elif group_name=="admins":
        role_caption = "Администратор"
    else:
        raise Exception("send_email_about_new_user: invalid user.groups")

    text_content = (
        f"Уважаемый {user.first_name}!\n"
        f"Вы зарегистрированы на сервисе как {role_caption}!\n"
        f"Логин: {user.username}\n"
        f"Пароль: {password}"
    )
    html_content = (
        f"Уважаемый {user.first_name}!<br>"
        f"Вы зарегистрированы на сервисе как {role_caption}!<br>"
        f"Логин: {user.username}\n"
        f"Пароль: {password}"
    ) 

    subject = f"Регистрация"

    msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_email_about_slot_action(slot_action):
    if slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_NEW:
        to_user = slot_action.slot.specialist
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Слот {slot_action.slot.pk} успешно создан!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Слот {slot_action.slot.pk} успешно создан!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_SIGN:
        to_user = slot_action.slot.specialist
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Пользователь {slot_action.slot.client.username} оставил заявке на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Пользователь {slot_action.slot.client.username} оставил заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_UNSIGN:
        to_user = slot_action.slot.specialist
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Пользователь {slot_action.client.username} отменил заявку на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Пользователь {slot_action.client.username} отменил заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_ACCEPT:
        to_user = slot_action.slot.client
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Специалист {slot_action.slot.specialist.username} одобрил Вашу заявку на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Специалист {slot_action.slot.specialist.username} одобрил Вашу заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_DECLINE:
        to_user = slot_action.client
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Специалист {slot_action.slot.specialist.username} отклонил Вашу заявку на {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Специалист {slot_action.slot.specialist.username} отклонил Вашу заявку на {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_DELETE:
        client = slot_action.slot.client
        if client:            
            to_user = client
            text_content = (
                f"Уважаемый {to_user.username}!\n"
                f"Специалист {slot_action.slot.specialist.username} отменил слот {slot_action.slot.pk}!"
            )
            html_content = (
                f"Уважаемый {to_user.username}!<br>"
                f"Специалист {slot_action.slot.specialist.username} отменил слот {slot_action.slot.pk}!"
            )
        else:
            to_user = None
    else:
        return
    
    if not to_user:
        return

    subject = f"Изменено состояние слота {slot_action.slot.pk}"

    msg = EmailMultiAlternatives(subject, text_content, None, [to_user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
