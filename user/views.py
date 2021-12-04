from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User


class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        print("POST 요청이 들어옴")

        email = request.data.get('email')  # 인풋에서 이메일 가져오기
        name = request.data.get('name')  # 인풋에서 이름 가져오기
        nickname = request.data.get('nickname')  # 인풋에서 닉네임 가져오기
        password = request.data.get('password')  # 인풋에서 비밀번호 가져오기
        profile_image = ''
        User.objects.create(email=email,
                            name=name,
                            nickname=nickname,
                            password=password,
                            profile_image=profile_image)

        return Response(status=200, data=dict(message="회원가입에 성공했습니다."))


class Login(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        print("POST 요청이 들어옴")

        email = request.data.get('email')  # 인풋에서 이메일 가져오기
        password = request.data.get('password')  # 인풋에서 비밀번호 가져오기
        # email의 회원이 있는지 검사
        # password == input password ?

        return Response(status=200, data=dict(message="회원가입에 성공했습니다."))
