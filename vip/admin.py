from django.contrib import admin
from .models import *


# Register your models here.

class vipAdmin(admin.ModelAdmin):
  list_display=('title','organizer_email', 'vip_date')
  prepopulated_fields={'slug':('title',)}
  list_filter=('title','vip_date',)

admin.site.register(myUser)
admin.site.register(Participant)
admin.site.register(vip, vipAdmin)
admin.site.register(Speaker)

