import requests
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User

# 테스트
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
        return render(request, 'user/login.html')

    def post(self, request):
        input_email = request.data.get('email')  # 인풋에서 이메일 가져오기
        input_password = request.data.get('password')  # 인풋에서 비밀번호 가져오기
        # 여기까지가 화면에서 올라온 email과 password를 저장

        # 1. email과 똑같은 email이 user_user테이블에 있나?
        if User.objects.filter(email=input_email).exists(): # 테이블에 있으면 True, False
            # 회원정보를 찾았어 find_user = 우리가 찾은사람
            find_user = User.objects.filter(email=input_email).first()
            # find_user.password = DB 테이블에 저장된 비밀번호
            if find_user.password == input_password:  # == 같으면 True, 틀리면 False
                # 비밀번호가 맞은경우 = 로그인 성공

                request.session['email'] = find_user.email
                request.session['login_check'] = True

                return Response(status=200, data=dict(message="로그인 성공"))

            else:
                # 비밀번호가 틀린경우
                return Response(status=400, data=dict(message="비밀번호가 틀렸습니다."))

        else:
            # 회원정보를 못찾았어
            return Response(status=404, data=dict(message="회원정보가 없습니다."))


class KakaoLogin(APIView):
    def get(self, request):
        app_rest_api_key = '1746262f9558a484e46e7c3cf0884a45'
        redirect_uri = "http://localhost:8000/kakao/callback/"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
        )


class KakaoCallBack(APIView):
    def get(self, request):
        app_rest_api_key = '1746262f9558a484e46e7c3cf0884a45'
        redirect_uri = "http://localhost:8000/kakao/callback/"
        user_token = request.GET.get("code")
        # post request
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        token_response_json = token_request.json()
        access_token = token_response_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print(profile_json)
        # parsing profile json
        id = profile_json.get("id")
        properties = profile_json.get("properties")
        nickname = properties.get('nickname')
        user_in_db = User.objects.filter(email=id).first()
        if user_in_db is None:
            # 화원가입
            user_in_db = User.objects.create(email=id, password=id, nickname=nickname, name=nickname, profile_image='')

        # 로그인
        request.session['email'] = user_in_db.email
        request.session['login_check'] = True
        return render(request, 'learningspoons/main.html')

