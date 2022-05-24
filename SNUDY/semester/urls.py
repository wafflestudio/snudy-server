from django.urls import path, include
from rest_framework.routers import SimpleRouter

from semester.views import SemesterCreateView, SemesterDeleteView

router = SimpleRouter()

urlpatterns = [
    path("semester/", SemesterCreateView.as_view(), name="semester_create"),            # /api/v1/semester/
    path("semester/<int:pk>/", SemesterDeleteView.as_view(), name="semester_delete"),   # /api/v1/semester/{id}/
    path("", include(router.urls)),
]
