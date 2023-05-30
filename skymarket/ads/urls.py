from django.urls import include, path
from rest_framework import routers

from ads.views import AdViewSet, CommentViewSet, UserAdsListViewSet

# TODO настройка роутов для модели

ad_router = routers.SimpleRouter()
ad_router.register('ads', viewset=AdViewSet)

comment_router = routers.SimpleRouter()
comment_router.register('ads/<int:ad_pk>/comments', viewset=CommentViewSet)

urlpatterns = [
    path('ads/me/', UserAdsListViewSet.as_view(), name='user_ads')
]

urlpatterns += ad_router.urls
urlpatterns += comment_router.urls
