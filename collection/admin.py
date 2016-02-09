from django.contrib import admin

# import model
from collection.models import Service

# set up automated slug creation
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug':('name',)}

# register model
admin.site.register(Service, ServiceAdmin)



