from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet, RegistryView, JWTTokenView

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)

# router_v1.register(
#     r'genres/(?P<slug>\w?)/comments',
#     CommentViewSet,
#     basename='comment'
# )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', RegistryView.as_view(), name='registry'),
    path('v1/auth/token/', JWTTokenView.as_view(), name='get_token')
]

