"""
URL configuration for smart_inventory_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    return JsonResponse({
        'message': 'Welcome to the Smart Inventory and Financial Tracking API',
        'description': 'A REST API for managing inventory and financial operations for SMEs.',
        'author': 'Mayo Takémsi Norris KADANGA',
        'version': '1.0.0',
        'documentation': request.build_absolute_uri('/api/docs/'),
        'endpoints': {
            'auth': {
                'register':        request.build_absolute_uri('/api/auth/register/'),
                'login':           request.build_absolute_uri('/api/auth/login/'),
                'refresh':         request.build_absolute_uri('/api/auth/refresh/'),
                'profile':         request.build_absolute_uri('/api/auth/me/'),
            },
            'inventory': {
                'products':        request.build_absolute_uri('/api/products/'),
                'categories':      request.build_absolute_uri('/api/categories/'),
            },
            'partners': {
                'suppliers':       request.build_absolute_uri('/api/suppliers/'),
                'customers':       request.build_absolute_uri('/api/customers/'),
            },
            'transactions':        request.build_absolute_uri('/api/transactions/'),
            'reports': {
                'stock_summary':        request.build_absolute_uri('/api/reports/stock-summary/'),
                'inventory_valuation':  request.build_absolute_uri('/api/reports/inventory-valuation/'),
                'low_stock':            request.build_absolute_uri('/api/reports/low-stock/'),
                'profit':               request.build_absolute_uri('/api/reports/profit/'),
            },
        },
        'hint': 'Visit /api/docs/ to explore and test all endpoints interactively.',
    })


urlpatterns = [
    path('',          api_root,   name='api-root'),
    path('admin/',    admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/',      include('inventory.urls')),
    path('api/',      include('partners.urls')),
    path('api/',      include('transactions.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/schema/',  SpectacularAPIView.as_view(),                       name='schema'),
    path('api/docs/',    SpectacularSwaggerView.as_view(url_name='schema'),  name='swagger-ui'),
]