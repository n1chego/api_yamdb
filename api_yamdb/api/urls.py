from django.urls import include, path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewViewSet, TitleViewSet
)


app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path(
        'v1/',
        include(router_v1.urls)
    ),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    # path('v1/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    # path('v1/', include('djoser.urls.jwt')),
]
