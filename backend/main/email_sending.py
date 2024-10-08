from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import mail_managers, EmailMultiAlternatives

from .models import SlotAction, SlotStatusActionType
# from .models import SchedulingMailData

def send_email_about_slot_action(slot_action):
    if slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_NEW:
        to_user = slot_action.slot.specialist.user
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Слот {slot_action.slot.pk} успешно создан!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Слот {slot_action.slot.pk} успешно создан!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_SIGN:
        to_user = slot_action.slot.specialist.user
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Пользователь {slot_action.slot.client.user.username} оставил заявке на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Пользователь {slot_action.slot.client.user.username} оставил заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_UNSIGN:
        # print(f"slot_action.slot.specialist={slot_action.slot.specialist}")
        # print(f"slot_action.slot.specialist.user={slot_action.slot.specialist.user}")
        to_user = slot_action.slot.specialist.user
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Пользователь {slot_action.client.user.username} отменил заявку на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Пользователь {slot_action.client.user.username} отменил заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_ACCEPT:
        to_user = slot_action.slot.client.user
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Специалист {slot_action.slot.specialist.user.username} одобрил Вашу заявку на слот {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Специалист {slot_action.slot.specialist.user.username} одобрил Вашу заявку на слот {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_DECLINE:
        to_user = slot_action.client.user
        text_content = (
            f"Уважаемый {to_user.username}!\n"
            f"Специалист {slot_action.slot.specialist.user.username} отклонил Вашу заявку на {slot_action.slot.pk}!"
        )
        html_content = (
            f"Уважаемый {to_user.username}!<br>"
            f"Специалист {slot_action.slot.specialist.user.username} отклонил Вашу заявку на {slot_action.slot.pk}!"
        )
    elif slot_action.status == SlotStatusActionType.SLOT_STATUS_ACTION_DELETE:
        client = slot_action.slot.client
        if client:            
            to_user = client.user
            text_content = (
                f"Уважаемый {to_user.username}!\n"
                f"Специалист {slot_action.slot.specialist.user.username} отменил слот {slot_action.slot.pk}!"
            )
            html_content = (
                f"Уважаемый {to_user.username}!<br>"
                f"Специалист {slot_action.slot.specialist.user.username} отменил слот {slot_action.slot.pk}!"
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
