from django.db.models import Q

from main.models import *    

def to_int(str_value, def_value):
    if str_value.isdigit():
        return int(str_value)
    else:
        return def_value

def get_slot_queryset(request, is_only_available=True):
    user = request.user
    if not Client.is_own(user):
        return Slot.objects.none()
    
    client = user.client

    specialist_id = to_int(request.GET.get('specialist', ''), -1)

    res = Slot.objects.all().exclude(is_deleted=True)

    if not (specialist_id == -1):
        res = res.filter(specialist=specialist_id)
    if is_only_available:
        # res = res.filter(client=None)
        res = res.filter(Q(client=None) | Q(client=client))

    # print(f"res.count()={res.count()}")

    return res