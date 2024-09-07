from main.models import *    

def to_int(str_value, def_value):
    if str_value.isdigit():
        return int(str_value)
    else:
        return def_value

def get_slot_queryset(request, is_only_available=True):
    user = request.user

    specialist_id = -1
    if Specialist.is_own(user):
        specialist_id = user.specialist.id
    else:
        specialist_id = to_int(request.GET.get('specialist', ''), -1)

    print("specialist=", specialist_id)

    res = Slot.objects.all()

    if not (specialist_id == -1):
        res = res.filter(specialist=specialist_id)
    if is_only_available:
        res = res.filter(client=None)

    return res