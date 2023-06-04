from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filter import AdFilter
from .models import Ad, Comment
from .permissions import IsOwner
from .serializers import AdDetailSerializer, AdSerializer, CommentSerializer, AdUpdateSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.filter(is_active=True).all()
    serializers = {
        "retrieve": AdDetailSerializer,
        'update': AdUpdateSerializer,
        'partial_update': AdUpdateSerializer,
    }
    default_serializer = AdSerializer
    filterset_class = AdFilter

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        if self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.select_related('author')
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_active = False
        item.save()
        comments = Comment.objects.filter(ad=item).all()
        for comment in comments:
            comment.is_active = False
            comment.save()

        return Response({}, status=204)


class UserAdsListViewSet(ListAPIView):
    queryset = Ad.objects.filter(is_active=True).all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(author=request.user)
        return super().list(request, *args, **kwargs)


class CommentListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True).all()
    serializer_class = CommentSerializer
    pagination_class = CommentListPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'create', 'list']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        self.queryset = self.queryset.filter(ad_id=ad_id)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        user_id = request.user.id
        request.data['ad'] = ad_id
        request.data['author'] = user_id
        print(request.data)
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
