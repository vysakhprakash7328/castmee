from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('Talent_user_registration_API/',views.Talent_user_registration_API.as_view()),
    path('TalentLogin_API/',views.TalentLogin_API.as_view()),
    path('Get_talent_user_details_API/',views.Get_talent_user_details_API.as_view()),
    path('TalentRecruiterRegistrationAPI/',views.TalentRecruiterRegistrationAPI.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]