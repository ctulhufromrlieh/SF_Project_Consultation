from main.permissions import CodeNamePermission

class ViewSpecPermission(CodeNamePermission):
    codename = "clients.view_spec"

class ViewSlotPermission(CodeNamePermission):
    codename = "clients.view_slot"

class ViewSlotActionPermission(CodeNamePermission):
    codename = "clients.view_slot_action"

class SignSlotActionPermission(CodeNamePermission):
    codename = "clients.sign_slot"

class UnsignSlotActionPermission(CodeNamePermission):
    codename = "clients.unsign_slot"
