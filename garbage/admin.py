from django.contrib import admin

from garbage.models import GarbageObject


class GarbageObjectAdmin(admin.ModelAdmin):
    list_display = ["name", "upload_date", "attachment"]
    search_fields = ["name"]


admin.site.register(GarbageObject, GarbageObjectAdmin)
