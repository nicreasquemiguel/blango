from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from blango_auth.models import User
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import Http404


class PostViewSet(viewsets.ModelViewSet):
    # we'll still refer to this in `get_queryset()`
    queryset = Post.objects.all()

    def get_queryset(self):
      # queryset has been set by applying user filtering rules

      # fetch the period_name URL parameter from self.kwargs
      time_period_name = self.kwargs.get("period_name")

      if not time_period_name:
          # no further filtering required
          return queryset

      if time_period_name == "new":
          return queryset.filter(published_at__gte=timezone.now() - timedelta(hours=1))
      elif time_period_name == "today":
          return queryset.filter(
              published_at__date=timezone.now().date(),
          )
      elif time_period_name == "week":
          return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
      else:
          raise Http404(
              f"Time period {time_period_name} is not valid, should be "
              f"'new', 'today' or 'week'"
          )

    @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers("Authorization", "Cookie"))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)
    # other methods/attributes omitte



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    @action(methods=["get"], detail=True, name="Posts with the Tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

class PostList(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]


    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    
class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer