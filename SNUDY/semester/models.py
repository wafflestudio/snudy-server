from django.db import models

from user.models import User


class Semester(models.Model):           # only can be created by admin
    TYPE = (
        ('FIRST', '1st'),
        ('SECOND', '2nd'),
        ('SUMMER', 'summer'),
        ('WINTER', 'winter')
    )

    type = models.CharField(choices=TYPE, max_length=10)
    year = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['type', 'year'],
                name='unique semester'
            )
        ]


class UserSemester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'semester'],
                name='unique user_semester'
            )
        ]