from django.contrib import admin
from django.urls import path,include

from customUser.views import UserLoginView

from poController.views import POGaurdView, POGaurdViewDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/poguard/', POGaurdView.as_view(), name='poguard'),
    path('api/poguard/<int:identifier>/', POGaurdViewDetail.as_view(), name='poguard details'),
]
