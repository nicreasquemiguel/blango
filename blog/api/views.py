from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from blango_auth.models import User
from blog.api.serializers import PostSerializer, UserSerializer
from blog.models import Post
from rest_framework.permissions import IsAuthenticated
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject


class PostList(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]


    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer