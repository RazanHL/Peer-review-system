from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('', include('pages.urls')),
    path('profiles/', include('profiles.urls')),
    path("accounts/", include('allauth.urls')),
    path("articles/", include('articles.urls')),
    path('predictions/', include('mlapplications.urls')),
    path('reviews/', include('reviews.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
