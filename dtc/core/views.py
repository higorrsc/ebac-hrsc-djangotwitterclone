from django.views.generic import CreateView, ListView, RedirectView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, PostForm
from .models import Post, Follow


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_invalid(self, form):
        # Você pode adicionar qualquer lógica adicional aqui se necessário
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
    pattern_name = "profile"

    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get("username")
        user_to_follow = User.objects.get(username=username)
        Follow.objects.get_or_create(
            follower=self.request.user, following=user_to_follow
        )
        return super().get_redirect_url(*args, **kwargs)


class LikePostView(LoginRequiredMixin, RedirectView):
    pattern_name = "index"  # Nome da URL para redirecionamento

    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        if self.request.user in post.likes.all():
            post.likes.remove(self.request.user)
        else:
            post.likes.add(self.request.user)
        # Redireciona para a URL sem parâmetros
        return super().get_redirect_url(*args, **kwargs)


class ProfileView(DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(user=self.object).order_by("-created_at")
        return context
