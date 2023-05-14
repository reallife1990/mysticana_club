from django.contrib import admin

# Register your models here.
from django.contrib import admin
from workplaceapp.models import MainClients, ServiceClients



# #@admin.register(User)
# class AdminMainClients(admin.ModelAdmin):
#     list_display = __all__
    #search_fields = ['first_name', 'last_name', 'email']

    # def client(self, obj):
    #     if obj.id_client is None:
    #         return False
    #     else:
    #         return True

# admin.site.register(MainClients)

class AdminClients(admin.ModelAdmin):
    list_display =['admin_name','age', 'born_date','user']
    pass

class AdminServiceClients(admin.ModelAdmin):
    empty_value_display = "unknown"
    list_display =[ 'client','service','date',]

    pass
#



admin.site.register(MainClients, AdminClients)
admin.site.register(ServiceClients, AdminServiceClients)#( сначала МОДЕЛЬ потом КЛАСС АДМ)
