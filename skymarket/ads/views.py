from rest_framework import pagination, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Ad, Comment
from .serializers import AdDetailSerializer, AdSerializer, CommentSerializer


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.filter(is_active=True).all()
    serializers = {
        "retrieve": AdDetailSerializer,
    }
    default_serializer = AdSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.select_related('author')
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_active = False
        item.save()
        return Response({'status': 'ok'}, status=204)


class UserAdsListViewSet(ListAPIView):
    queryset = Ad.objects.filter(is_active=True).all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(author=request.user)
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True).all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        user_id = request.user.id
        request.data['ad_id'] = ad_id
        request.data['author_id'] = user_id
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        comment = self.get_object()
        comment.is_active = False
        comment.save()
        return Response({'status': 'ok'}, status=204)
