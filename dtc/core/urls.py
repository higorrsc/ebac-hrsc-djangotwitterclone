from django.urls import path

from .views import PostCreateView, FollowUserView, LikePostView, PostsView

urlpatterns = [
    path("", PostsView.as_view(), name="posts"),
    path("new_post/", PostCreateView.as_view(), name="new_post"),
    path("follow/<str:username>/", FollowUserView.as_view(), name="follow_user"),
    path("like/<int:post_id>/", LikePostView.as_view(), name="like_post"),
]
