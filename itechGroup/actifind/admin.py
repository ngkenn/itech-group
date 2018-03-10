from django.contrib import admin
from actifind.models import Activity, Review, Picture

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display=('title', 'activity', 'url')

admin.site.register(Review, ReviewAdmin)
