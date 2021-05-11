from django.urls import path,include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register('meetings', views.MeetingsViewSet)
router.register('calender', views.CalenderEventsViewSet)
router.register('profiles', views.UserProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('login/', views.CustomLoginView.as_view()),
    path('auth/registration/', include('dj_rest_auth.registration.urls'))
]
