from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

'''
This file defines all the URL patterns for the application and maps them to their respective views.
'''
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('how-we-do-it/', views.how_we_do_it, name='how_we_do_it'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_file, name='upload_file'),
    path('algorithm_selection_and_processing/', views.algorithm_selection, name='algorithm_selection'),
    path('processed/', views.processed_datasets, name='processed_datasets'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)