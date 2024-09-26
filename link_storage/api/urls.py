from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkDetailView, LinkListCreateView, CollectionListCreateView, CollectionDetailView
from .auth_views import RegisterView, PasswordChangeView, PasswordResetView, CustomLoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
]

