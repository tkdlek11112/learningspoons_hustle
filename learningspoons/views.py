from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Product
from user.models import User


class Main(APIView):
    def get(self, request):
        email = request.session.get('email')
        find_user = User.objects.filter(email=email).first()

        is_login = request.session.get('login_check', False)

        return render(request, 'learningspoons/main.html',
                      context=dict(
                          data_list=Product.objects.all().order_by('-id'),
                          user_info=find_user,
                          is_login=is_login
                      ))


class Search(APIView):
    def post(self, request):
        if request.session.get('login_check'):
            email = request.session.get('email')
            find_user = User.objects.filter(email=email).first()
            keyword = request.data.get('keyword')

            last_view_product_list = Product.objects.filter(id__in=request.session.get('last_view_list', []))

            return render(request, 'learningspoons/main.html',
                          context=dict(
                              data_list=Product.objects.filter(description__contains=keyword).order_by('-id'),
                              user_info=find_user,
                              last_view_product_list=last_view_product_list
                          ))
        else:
            return render(request, 'user/login.html')

