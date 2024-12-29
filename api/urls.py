from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import ProductListCreateView, InteractionView


urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path('products/<str:product_id>/interactions/',
         InteractionView.as_view(), name='product-interactions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
