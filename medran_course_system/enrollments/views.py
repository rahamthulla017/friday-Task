from rest_framework import viewsets, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.all()
