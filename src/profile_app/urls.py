from django.contrib import admin
from django.urls import path
from rest_framework import routers

from profiles.views.auth_views import AuthViews
from profiles.views.profile_views import ProfileViews

urlpatterns = [
    path("admin/", admin.site.urls),
]

auth_router = routers.SimpleRouter()
auth_router.register(r"auth", AuthViews, basename="auth")

profile_router = routers.SimpleRouter()
profile_router.register(r"profiles", ProfileViews, basename="profiles")

routers = [auth_router, profile_router]
for router in routers:
    urlpatterns += router.urls
