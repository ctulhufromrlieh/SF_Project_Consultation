from django.contrib import admin
from django.forms.models import *
from django.forms.fields import *

from django.core.exceptions import *
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User, Group

from .models import *
from .email_sending import *

class CustomUserCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    role_choices = [
        ("C", "Client"),
        ("S", "Specialist"),
        ("A", "Admin")
    ]

    role = ChoiceField(
        label="Role",
        choices=role_choices,
        help_text="User role",
    )

    class Meta:
        model = User
        fields = ("username", "email", "role")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username

    def save(self, commit=True):
        user = super().save(commit=False)

        chosen_role = self.cleaned_data["role"]
        if chosen_role == "C":
            group_name = "clients"
        elif chosen_role == "S":
            group_name = "specialists"
        elif chosen_role == "A":
            group_name = "admins"
        else:
            raise Exception("CustomUserCreationForm.save: invalid chosen_role")
        
        group = Group.objects.get(name=group_name)
        user.group_to_add = group

        password = User.objects.make_random_password()
        user.email = self.cleaned_data["email"]
        user.set_password(password)
        send_email_about_new_user(user, group_name, password)

        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "role"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if hasattr(obj, "group_to_add"):
            if obj.group_to_add:
                obj.groups.add(obj.group_to_add)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Slot)
admin.site.register(ConsultType)
admin.site.register(ReasonType)
