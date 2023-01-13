from django.contrib import admin
from authapp.models import User



#@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('first_name', 'date_joined', 'last_login','client')
    search_fields = ['first_name', 'last_name', 'email']

    def client(self, obj):
        if obj.id_client is None:
            return False
        else:
            return True

admin.site.register(User,AdminUser)