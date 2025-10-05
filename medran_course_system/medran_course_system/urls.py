from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from courses.views import CourseViewSet, index, courses_page, login_page
from enrollments.views import EnrollmentViewSet
from users.views import UserRegistrationView
from users.views import profile_page, register_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# DRF Router for APIs
router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # 🌐 Frontend Pages
    path('', index, name='index'),
    path('courses-page/', courses_page, name='courses_page'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),

    # 🧠 API Routes
    path('api/', include(router.urls)),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('register/', register_page, name='register_page'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
