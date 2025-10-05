from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer

# ----------------------------
# Frontend Pages
# ----------------------------

def index(request):
    """
    Homepage view
    """
    return render(request, 'index.html')


def courses_page(request):
    """
    Courses list page view
    """
    return render(request, 'courses.html')


def login_page(request):
    """
    Login/Register page view
    """
    return render(request, 'login.html')


# ----------------------------
# API Views
# ----------------------------

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Courses
    Supports role-based access:
      - Admin: sees all courses
      - Instructor: sees own courses
      - Student/Anonymous: sees only Approved courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        # Anonymous users: Only show approved courses
        if not user.is_authenticated:
            return Course.objects.filter(status='Approved')

        # Admin users: See all courses
        if user.is_staff:
            return Course.objects.all()

        # Instructors: See only their own courses
        if hasattr(user, 'role') and user.role == 'instructor':
            return Course.objects.filter(instructor=user)

        # Students: Only see approved courses
        return Course.objects.filter(status='Approved')

    # ----------------------------
    # Admin Actions
    # ----------------------------

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Approve a course (Admin only)
        """
        course = self.get_object()
        course.status = 'Approved'
        course.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Reject a course (Admin only)
        """
        course = self.get_object()
        course.status = 'Rejected'
        course.save()
        return Response({'status': 'rejected'})
