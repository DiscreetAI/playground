from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

from views.facebook_login import FacebookLogin

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Authentication API', description='RESTful API for Authentication.')),
    url(r'^auth/', include('rest_auth.urls')),
    #url(r'^auth/registration/', include('rest_auth.registration.urls'))
    path('admin/', admin.site.urls),
]
