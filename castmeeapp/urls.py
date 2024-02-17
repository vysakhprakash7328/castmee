from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('talent_user_registration_api/',views.Talent_user_registration_API.as_view()),
    path('login_api/',views.Login_API.as_view()),
    path('get_talent_user_details_api/',views.Get_talent_user_details_API.as_view()),
    path('talent_recruiter_registration_api/',views.TalentRecruiterRegistrationAPI.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]