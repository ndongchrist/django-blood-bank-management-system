"""
URL configuration for bloodBMS project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    path('cms/', include(wagtailadmin_urls)),  # Wagtail admin
    path('documents/', include(wagtaildocs_urls)),  # Wagtail document serving
    # Your other URLs...
    path('', include(wagtail_urls)),  # Wagtail page serving

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)