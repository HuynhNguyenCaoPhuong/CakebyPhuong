from django.urls import path
from django.conf.urls import handler404, handler500
from . import views


app_name = 'classes'
urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.course, name='course'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('single/<int:id>/', views.single, name='single'),
    path('blog/', views.blog, name='blog'),
    path('tip/<int:id>/', views.tip, name='tip'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('teacher/', views.teacher, name='teacher'),
    path('search_course/', views.search_course, name='search_course'),
    path('search_blog/', views.search_blog, name='search_blog'),
    # path('faqs/', views.faqs, name='faqs'),
]

