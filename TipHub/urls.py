
from django.contrib import admin
from django.urls import path, include
from index.views import homepage
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
    path("comments/", include('django_comments_xtd.urls')),
    path("notifications/", include('notification.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
