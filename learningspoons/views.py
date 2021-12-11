from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Feed
from user.models import User


class Main(APIView):
    def get(self, request):
        if request.session.get('login_check'):
            email = request.session.get('email')
            find_user = User.objects.filter(email=email).first()
            return render(request, 'learningspoons/main.html',
                          context=dict(
                              data_list=Feed.objects.all().order_by('-id'),
                              user_info=find_user
                          ))
        else:
            return render(request, 'user/login.html')



