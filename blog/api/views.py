from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from blog.api.serializers import PostSerializer
from blog.models import Post
from rest_framework.permissions import IsAuthenticated

class PostList(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    