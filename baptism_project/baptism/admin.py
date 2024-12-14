
from django.contrib import admin
from .models import Baptism,ParishDetails,LoginDetails,BaptismAdvanced,FieldTable
@admin.register(Baptism)
class BaptismAdmin(admin.ModelAdmin):
    list_display = (
        'basic_baptism_id', 'child_name_first', 'child_name_second',
        'place_of_baptism', 'date_of_baptism', 'status'
    )
    search_fields = ('child_name_first', 'child_name_second', 'place_of_baptism')
    list_filter = ('status', 'date_of_baptism')

@admin.register(ParishDetails)
class ParishDetailsAdmin(admin.ModelAdmin):
    list_display = ('parish_id', 'name_of_parish', 'place_of_parish', 'status', 'created_time')
    list_filter = ('status',)
    search_fields = ('name_of_parish', 'place_of_parish')




@admin.register(LoginDetails)
class LoginDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'contact_no', 'role', 'status', 'last_login', 'parish_id')
    search_fields = ('user_name', 'email', 'contact_no')
    list_filter = ('role', 'status', 'parish_id')
    ordering = ('-last_login',)

    fieldsets = (
        (None, {
            'fields': ('user_name', 'password', 'email', 'contact_no', 'role', 'status', 'parish_id')
        }),
        ('Timestamps', {
            'fields': ('last_login',)
        }),
    )
    readonly_fields = ('last_login',)  # Make last_login read-only in the admin panel

    def save_model(self, request, obj, form, change):
        """
        Override save_model to hash the password before saving in the admin panel.
        """
        if 'password' in form.changed_data:
            from django.contrib.auth.hashers import make_password
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)




@admin.register(BaptismAdvanced)
class BaptismAdvancedAdmin(admin.ModelAdmin):
    list_display = ('advanced_baptism_id', 'basic_baptism_id', 'question', 'question_type', 'compulsary', 'status', 'created_time')
    search_fields = ('question', 'question_type')
    list_filter = ('status', 'compulsary')
    ordering = ('-created_time',)



@admin.register(FieldTable)
class FieldTableAdmin(admin.ModelAdmin):
    list_display = ('field_id', 'order_no', 'type', 'q_id', 'status', 'created_time')
    list_filter = ('status', 'created_time')
    search_fields = ('type', 'data', 'choice')
