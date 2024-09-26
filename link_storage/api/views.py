from rest_framework import viewsets
from .models import Link, Collection
from .serializers import LinkSerializer, CollectionSerializer
from rest_framework.permissions import IsAuthenticated
import requests
from bs4 import BeautifulSoup
from rest_framework import generics, permissions
from .models import Link


class LinkListCreateView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        url = self.request.data.get('url')
        data = self.fetch_link_data(url)
        serializer.save(user=self.request.user, **data)

    def fetch_link_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else ''
            description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={
                'name': 'description'}) else ''
            image = soup.find('meta', property='og:image')['content'] if soup.find('meta', property='og:image') else ''
            link_type = soup.find('meta', property='og:type')['content'] if soup.find('meta',
                                                                                      property='og:type') else 'website'

            return {
                'title': title,
                'description': description,
                'image': image,
                'link_type': link_type,
                'url': url
            }
        except Exception as e:
            return {
                'title': 'Untitled',
                'description': '',
                'image': '',
                'link_type': 'website',
                'url': url
            }


class LinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class CollectionListCreateView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)
