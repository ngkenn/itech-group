from django.contrib import admin
from actifind.models import Activity, Review, Picture
from actifind.models import UserProfile

# Register your models here.


#class ReviewAdmin(admin.ModelAdmin):
#     list_display=('title', 'activity', 'url')

class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(UserProfile)
admin.site.register(Activity, ActivityAdmin)
#admin.site.register(Review, ReviewAdmin)
