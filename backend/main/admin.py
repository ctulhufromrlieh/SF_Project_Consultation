from django.contrib import admin
from django.forms.models import *
from django.forms.fields import *

from django.core.exceptions import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User, Group

# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.exceptions import ValidationError
# from .models import User

from .models import *
from .email_sending import *

# class CustomUserCreationForm(UserCreationForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     class Meta:
#         model = User
#         fields = ["username"]
#         exclude = ["password1", "password2"]
# UserCreationForm

class CustomUserCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    # error_messages = {
    #     "password_mismatch": _("The two password fields didn’t match."),
    # }
    # password1 = CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    #     help_text=password_validation.password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     label=_("Password confirmation"),
    #     widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    #     strip=False,
    #     help_text=_("Enter the same password as before, for verification."),
    # )

    role_choices = [
        ("C", "Client"),
        ("S", "Specialist"),
        ("A", "Admin")
    ]

    role = ChoiceField(
        label="Role",
        choices=role_choices,
        # strip=False,
        # widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError(
    #             self.error_messages["password_mismatch"],
    #             code="password_mismatch",
    #         )
    #     return password2

    # def _post_clean(self):
    #     super()._post_clean()
    #     # Validate the password after self.instance is updated with form data
    #     # by super().
    #     password = self.cleaned_data.get("password2")
    #     if password:
    #         try:
    #             password_validation.validate_password(password, self.instance)
    #         except ValidationError as error:
    #             self.add_error("password2", error)

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
        # user.groups.add(group)

        password = User.objects.make_random_password()
        user.email = self.cleaned_data["email"]
        user.set_password(password)
        send_email_about_new_user(user, group_name, password)
        # print(password)
        if commit:
            user.save()
            # user.groups.add(group) #
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
        if obj.group_to_add:
            obj.groups.add(obj.group_to_add)

# Register your models here.
# admin.site.register(Client)
# admin.site.register(Specialist)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Slot)