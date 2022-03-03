from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import Response, APIView
import os


class PingAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, *args, **kwargs):
        return Response({
            'ping': 'pong'
        })