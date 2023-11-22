from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('list', views.list, name='list'),
    path('edit/fileupload', views.fileupload, name='fileupload'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit/update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/prescription', views.prescription, name='prescription'),
    path('edit/delete', views.delete_prescription, name='delete_prescription'),
    path('edit/getprescription', views.getprescription, name='getprescription'),
    path('register', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('users/', views.users, name='users'),
    path('users/delete/<int:id>', views.user_delete, name='user_delete'),
    path('change_password', views.changePassword, name='changePassword'),
    path('password/delete', views.changePassword, name='changePassword'),
    path('edit/deleteFile/<int:id>/<int:patient_id>', views.deleteFiles, name='deleteFiles'),
]

