"""Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name="index"),
    path('accounts/login/',views.login_page,name='login'),
    path('accounts/logout/',views.logout_page,name='logout'),
    path('accounts/register', views.register_page, name='register'),
    path('events/<str:id>/', views.event_page, name="event_page"),
    path('register_confirm/<str:id>/', views.register_confirm, name="register_confirm"),
    path('user-profile/<str:id>',views.profile_page,name='user-profile'),
    path('user-account/',views.account_page,name='account-page'),
    path('submit-project/<str:id>/', views.submit_form, name='submit-project'),
    path('update-project/<str:id>/', views.update_form, name='update-form'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('password-change/', views.password_change, name='password-change')
]