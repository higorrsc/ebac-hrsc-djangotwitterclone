from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.urls import views as auth_views
from django.urls import include, path

from core.views import RegisterView

urlpatterns = (
    [
        path(
            "",
            include("core.urls"),
        ),
        path(
            "admin/",
            admin.site.urls,
            name="admin",
        ),
        path(
            "accounts/",
            include("django.contrib.auth.urls"),
            name="accounts",
        ),
        path(
            "accounts/logout_new/",
            auth_views.LogoutView.as_view(http_method_names=["post", "get", "options"]),
            name="logout_new",
        ),
        path(
            "accounts/register/",
            RegisterView.as_view(),
            name="register",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
