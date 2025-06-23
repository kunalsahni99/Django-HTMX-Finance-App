from django.contrib import admin
from django.urls import path, include
from finance_project import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('tracker.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]