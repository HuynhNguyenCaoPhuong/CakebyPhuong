"""CakebyPhuong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView

admin.site.site_header = "Trang quản trị viên của CakebyPhuong"
admin.site.index_title = "CakebyPhuong admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classes.urls')),
    # path('', include('cart.urls')),
    path('users/', include('users.urls')),
    re_path(r'^ckeditor/',include('ckeditor_uploader.urls')),
    # path('static/js/main.js', TemplateView.as_view(template_name='main.js', content_type='application/javascript'), name='main_js'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler301 = 'classes.views.custom_301'
handler403 = 'classes.views.custom_403'
handler404 = 'classes.views.custom_404'
handler505 = 'classes.views.custom_505'