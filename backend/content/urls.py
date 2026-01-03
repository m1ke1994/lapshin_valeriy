from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactRequestViewSet, SiteContentView

router = DefaultRouter()
router.register(r"applications", ContactRequestViewSet, basename="application")

urlpatterns = [
    path("site/", SiteContentView.as_view(), name="site-content"),
    path("", include(router.urls)),
]
