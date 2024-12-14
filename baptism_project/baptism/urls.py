from django.urls import path
from .views import (
    baptism_form_view, 
    upload_parish_details, 
    success_page, 
    login_view, 
    register_view, 
    upload_baptism_advanced, 
    upload_field_table,
    field_table_list, 
    field_table_add, 
    field_table_edit, 
    field_table_delete,
    baptism_advanced_list, 
    baptism_advanced_add, 
    baptism_advanced_edit, 
    baptism_advanced_delete,
    parish_details_list,
    parish_details_add,
    parish_details_edit,
    parish_details_delete,
    baptism_list,
    baptism_add,
    baptism_edit,
    baptism_delete
)

urlpatterns = [
    # Existing URLs
    path('add/', baptism_form_view, name='add_baptism'),
    path('', baptism_form_view, name='baptism_home'), 
    path('upload-parish/', upload_parish_details, name='upload_parish'),
    path('parish-success/', success_page, name='parish_success'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('upload-baptism-advanced/', upload_baptism_advanced, name='upload_baptism_advanced'),
    path('upload-field/', upload_field_table, name='upload_field'),
    path('field-table-success/', success_page, name='field_table_success'), 

    # FieldTable URLs
    path('field_table_list/', field_table_list, name='field_table_list'),
    path('fields/', field_table_list, name='field_list'), 
    path('fields/add/', field_table_add, name='field_add'), 
    path('fields/edit/<int:pk>/', field_table_edit, name='field_table_edit'),
    path('fields/delete/<int:field_id>/', field_table_delete, name='field_delete'),

    # BaptismAdvanced URLs
    path('baptism-advanced/', baptism_advanced_list, name='baptism_advanced_list'),  # Listing page
    path('baptism-advanced/add/', baptism_advanced_add, name='baptism_advanced_add'),  # Add page
    path('baptism-advanced/edit/<int:pk>/', baptism_advanced_edit, name='baptism_advanced_edit'),  # Edit page
    path('baptism-advanced/delete/<int:advanced_baptism_id>/', baptism_advanced_delete, name='baptism_advanced_delete'),  # Delete page


    path('parishes/', parish_details_list, name='parish_details_list'),
    path('parishes/add/', parish_details_add, name='parish_details_add'),
    path('parishes/edit/<int:pk>/', parish_details_edit, name='parish_details_edit'),
    path('parishes/delete/<int:parish_id>/', parish_details_delete, name='parish_details_delete'),

    path('baptisms/', baptism_list, name='baptism_list'),  # List baptisms
    path('baptisms/add/', baptism_add, name='baptism_add'),  # Add new baptism
    path('baptisms/edit/<int:pk>/', baptism_edit, name='baptism_edit'),  # Edit existing baptism
    path('baptisms/delete/<int:baptism_id>/', baptism_delete, name='baptism_delete'),  # Delete     


]
