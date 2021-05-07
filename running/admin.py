from django.contrib import admin

# Register your models here.
from .models import Area, Cities, Countries, Regions, States, Continents

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Countries)
class CountryAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name')


@admin.register(States)
class StateAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name')

# @admin.register(Countries)
class CityAdmin(ReadOnlyAdmin):
    # list_display = ('city_id', 'country_id',  'state_id', 'cname', 'name')
    # search_fields = ('chn_name', 'eng_name')
    autocomplete_fields = ['state_id', 'country_id']
    # autocomplete_fields = ['country_id']


admin.site.register(Area)
admin.site.register(Cities, CityAdmin)
# admin.site.register(Countries)
admin.site.register(Regions)
# admin.site.register(States)
admin.site.register(Continents, ReadOnlyAdmin)