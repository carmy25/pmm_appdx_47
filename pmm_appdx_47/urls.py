"""
URL configuration for pmm_appdx_47 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

admin.site.site_header = "ПММ GROK"
admin.site.site_title = "ПММ Grok"
admin.site.index_title = "Панель Адміністратора"

apps.get_app_config("constance").verbose_name = "Налаштування"

# admin.site.unregister(User)
# admin.site.unregister(Group)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("_nested_admin/", include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
