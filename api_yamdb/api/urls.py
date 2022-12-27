from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet


app_name = 'api'

router = SimpleRouter()
router.register(
    'titles',
    TitleViewSet
)
router.register(
    'genres',
    GenreViewSet
)
router.register(
    'categories',
    CategoryViewSet
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review>[\d]+)/comments/',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    # path('v1/', include('djoser.urls.jwt')),
]
