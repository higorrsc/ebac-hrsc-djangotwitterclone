from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, RedirectView, DetailView
from .forms import CustomUserCreationForm, PostForm
from .models import Post, Follow


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_invalid(self, form):
        return super().form_invalid(form)


class PostsView(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "new_post.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FollowUserView(LoginRequiredMixin, RedirectView):
    def post(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, pk=self.kwargs.get("pk"))
        is_following = Follow.objects.filter(
            follower=request.user, following=user_to_follow
        ).exists()
        if is_following:
            Follow.objects.filter(
                follower=request.user, following=user_to_follow
            ).delete()
        else:
            Follow.objects.create(follower=request.user, following=user_to_follow)

        return HttpResponseRedirect(
            reverse("profile", kwargs={"pk": user_to_follow.pk})
        )


class LikePostView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        if self.request.user in post.likes.all():
            post.likes.remove(self.request.user)
        else:
            post.likes.add(self.request.user)
        return self.request.META.get("HTTP_REFERER", reverse("posts"))


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        following = Follow.objects.filter(follower=user)
        followers = Follow.objects.filter(following=user)
        is_following = Follow.objects.filter(
            follower=self.request.user,
            following=self.get_object(),
        ).exists()
        context["is_following"] = is_following
        context["posts"] = Post.objects.filter(user=self.object).order_by("-created_at")
        context["following"] = [follow.following for follow in following]
        context["followers"] = [follow.follower for follow in followers]

        return context


class ProfileSearchView(ListView):
    model = User
    template_name = "search_result.html"
    context_object_name = "users"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return User.objects.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
        return User.objects.none()
