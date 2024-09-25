from rest_framework import viewsets
from .models import Link, Collection
from .serializers import LinkSerializer, CollectionSerializer
from rest_framework.permissions import IsAuthenticated


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    queryset = Link.objects.all()

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)
