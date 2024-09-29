from main.models import *    

def get_slot_queryset(request):
    user = request.user
    if not Specialist.is_own(user):
        return Slot.objects.none()    

    specialist_id = user.specialist.id
    # specialist_id = -1
    # if Specialist.is_own(user):
    #     specialist_id = user.specialist.id
    # else:
    #     specialist_id = to_int(request.GET.get('specialist', ''), -1)

    print("specialist=", specialist_id)

    res = Slot.objects.all()

    if not (specialist_id == -1):
        res = res.filter(specialist=specialist_id)
    # if is_only_available:
        # res = res.filter(client=None)

    return res