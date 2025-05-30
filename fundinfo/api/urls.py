from django.urls import path, include

urlpatterns = [
    path('users/', include(('fundinfo.users.urls', 'users'))),
    path('users/auth/', include(('fundinfo.authentication.urls', 'auth'))),
]
