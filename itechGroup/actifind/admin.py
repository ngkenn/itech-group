from django.contrib import admin
from actifind.models import Activity, Review, Picture
from actifind.models import UserProfile

# Register your models here.


# class ReviewAdmin(admin.ModelAdmin):
#     list_display=('title', 'activity', 'url')
#
# admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(Activity)
admin.site.register(Review)
admin.site.register(Picture)

