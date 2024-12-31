from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "pleasant_habit", "is_public", "periodicity")
    list_filter = ("pleasant_habit", "is_public")
    search_fields = ("action", "user__username")
    list_editable = ("pleasant_habit", "is_public")
    fieldsets = (
        (None, {
            "fields": ("user", "action", "place", "time", "pleasant_habit"),
        }),
        ("Дополнительная информация", {
            "fields": ("related_habit", "periodicity", "reward", "execution_time", "is_public"),
        }),
    )
    readonly_fields = ("user",)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("telegram_id",)}),
    )
    list_display = UserAdmin.list_display + ("telegram_id",)
    search_fields = UserAdmin.search_fields + ("telegram_id",)

admin.site.register(CustomUser, CustomUserAdmin)
