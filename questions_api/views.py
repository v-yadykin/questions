from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import requests

from questions_api import serializers
from questions_api import models

INTELLECT_API_URL = 'http://vega.fcyb.mirea.ru/intellectapi/'

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=tg_login',)
    permission_classes = (IsAdminUser,)

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=status',)


class GetResourceApiView(APIView):
    serializer_class = serializers.GetResourceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
        question_text = serializer.question.text
        data = {
            'phrase': question_text,
            'collection': 1,
            'batch-start': serializer.validated_data['batch_start'],
            'batch-size': serializer.validated_data['batch_size']
        }
        r = requests.post(INTELLECT_API_URL+'search-phrase', data=data)

        if not status.is_success(r.status_code):
            return Response('Failed to get resources', r.status_code)

        return Response({'question': question_text, **r.json()})