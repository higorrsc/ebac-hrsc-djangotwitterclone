from django.urls import path

from .views import (
    PostCreateView,
    FollowUserView,
    LikePostView,
    PostsView,
    ProfileView,
    ProfileSearchView,
)

urlpatterns = [
    path("", PostsView.as_view(), name="posts"),
    path("new_post/", PostCreateView.as_view(), name="new_post"),
    path("follow/<int:pk>/", FollowUserView.as_view(), name="follow_user"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("search/", ProfileSearchView.as_view(), name="search"),
    path("like/<int:post_id>/", LikePostView.as_view(), name="like_post"),
]
