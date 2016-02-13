from django.contrib import admin

# import model
from .models import Service
from .models import Price

# set up automated slug creation
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug':('name',)}

# register models
admin.site.register(Service, ServiceAdmin)
admin.site.register(Price)


