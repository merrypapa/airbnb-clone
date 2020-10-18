from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # . means in the same folder of the current file(admin.py)
from rooms import models as rooms_models


class RoomInline(admin.TabularInline):
    # other option: StackedInline
    model = rooms_models.Room


@admin.register(models.User)  # decorator: read the below command
class CustomUserAdmin(
    UserAdmin
):  # ModelAdmin class is the representation of a model in the admin interface

    """ Custom User Admin """

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Banana",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)


# Django Document Sample below
# from django.contrib import admin
# from myproject.myapp.models import Author

# class AuthorAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Author, AuthorAdmin)
