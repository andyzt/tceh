from django.contrib import admin

from djcelery.models import TaskMeta

from pizza.models import PizzaMenuItem, PizzaSize, PizzaOrderNotification

# Register your models here.


class PizzaSizeModel(admin.ModelAdmin):
    list_display = ('size', )

admin.site.register(PizzaSize, PizzaSizeModel)


class PizzaMenuItemModel(admin.ModelAdmin):
    def ingredients_list(self, obj):
        return ', '.join(i.name for i in obj.ingredients.all())
    ingredients_list.short_description = 'Ingredients'

    list_display = ('name', 'ingredients_list')

admin.site.register(PizzaMenuItem, PizzaMenuItemModel)


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result', )
admin.site.register(TaskMeta, TaskMetaAdmin)


admin.site.register(PizzaOrderNotification)
