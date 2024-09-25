from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, CollectionViewSet

router = DefaultRouter()
router.register('links', LinkViewSet)
router.register('collections', CollectionViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
