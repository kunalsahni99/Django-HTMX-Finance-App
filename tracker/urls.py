from django.urls import path, include
from tracker import views
import debug_toolbar
from finance_project import settings


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transactions_list, name='transactions-list'),
    path("transactions/create/", views.create_transaction, name='create-transaction'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]