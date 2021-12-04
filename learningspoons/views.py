from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Feed


class Main(APIView):
    def get(self, request):
        return render(request, 'learningspoons/main.html')
