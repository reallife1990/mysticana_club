from django.contrib import admin
from mainapp.models import News, Services, FormatService
# Register your models here.
admin.site.register(News)
admin.site.register(FormatService)
# admin.site.register(Services)
class AdminServices(admin.ModelAdmin):
    list_display = ['title', 'updated_at', 'price']


admin.site.register(Services,AdminServices)