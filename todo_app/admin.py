from django.contrib import admin

from todo_app.models import Todo

# Register your models here.
# admin.site.register([todo])
@admin.register(Todo)
class todoadmin(admin.ModelAdmin):
    list_display = ['id','name','title','date','created_at']
    search_field = ['title','name', 'id','date','created']