from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkDetailView, LinkListCreateView, CollectionListCreateView, CollectionDetailView
from .auth_views import RegisterView, PasswordChangeView, PasswordResetView, CustomLoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Link and Collection API",
        default_version='v1',
        description="Документация для API управления ссылками и коллекциями",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('links', LinkListCreateView, basename='link')
router.register('collections', CollectionListCreateView, basename='collection')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('links/', LinkListCreateView.as_view(), name='link-list-create'),
    path('links/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),
    #path('collections/', CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
