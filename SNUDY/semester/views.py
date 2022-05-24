from django.db import IntegrityError
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from semester.models import Semester
from semester.serializers import SemesterSerializer


class SemesterCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )


    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'year': openapi.Schema(type=openapi.TYPE_INTEGER, description='year'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='type'),
        }
    )
    responses = {
        201: 'Successfully create semester',
        400: 'Invalid input data: no year or no type',
        401: 'Unauthorized user',
        403: 'Only for admin',
        405: 'Method not allowed: POST or DELETE',
        409: 'Already created semester',
        500: 'Internal server error'
    }

    @swagger_auto_schema(tags=["Semester"], request_body=request_body, responses=responses)
    def post(self, request):
        me = request.user
        if not me.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'only created by admin'})
        serializer = SemesterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data={'message': 'already created semester'})
        return Response(status=status.HTTP_201_CREATED, data={'message': 'successfully create semester'})


class SemesterDeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    responses = {
        200: 'Successfully delete tweet',
        401: 'Unauthorized user',
        403: 'Only for admin',
        404: 'Not found: no such semester exists',
        405: 'Method not allowed: POST or DELETE',
        500: 'Internal server error'
    }

    @swagger_auto_schema(tags=["Semester"], responses=responses)
    def delete(self, request, pk):
        me = request.user
        if not me.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'only deleted by admin'})

        semester = get_object_or_404(Semester, pk=pk)
        semester.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'successfully delete semester'})