from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext
from .models import ProfileImage

User = get_user_model()


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    can_delete = True
    verbose_name_plural = gettext("Profile Image")
    fk_name = "user"

@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileImageInline]
    list_display = ['image','username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


    def image(self, obj):
        profile_image = obj.profile_image()
        print(profile_image)
        if profile_image:
            url = reverse("admin:authentication_user_change", args=[obj.id])
            return format_html('<a href="{}"><img src="{}" height="30" style="border-radius: 50%;"/></a>', url, profile_image)
        else:
            return gettext("No Image")
    image.short_description = gettext("Image")


