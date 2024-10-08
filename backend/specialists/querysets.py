from main.models import *    

def get_slot_queryset(request):
    user = request.user
    if not Specialist.is_own(user):
        return Slot.objects.none()    

    specialist_id = user.specialist.id

    res = Slot.objects.all().exclude(is_deleted=True)

    if not (specialist_id == -1):
        res = res.filter(specialist=specialist_id)
    # if is_only_available:
        # res = res.filter(client=None)

    return res