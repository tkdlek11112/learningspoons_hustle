import requests
from django.shortcuts import render, redirect
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
                            profile_image=profile_image,
                            )
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


class Logout(APIView):
    def post(self, request):
        request.session.flush()
        return Response(status=200)


class KakaoLogin(APIView):
    def get(self, request):
        print(request.get_host())
        app_rest_api_key = '957ed2afa5eff369f7e405795df71fcd'
        redirect_uri = "http://" + request.get_host() + "/kakao/oauth"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
        )


class KakaoCallBack(APIView):
    def get(self, request):
        # 카카오 개발자 홈페이지의 REST KEY
        app_rest_api_key = '957ed2afa5eff369f7e405795df71fcd'
        # 카카오 개발자 홈페이지의 리다이렉트 URL
        redirect_uri = "http://" + request.get_host() + "/kakao/oauth"

        # 카카오 로그인에 호출 성공하면 인가코드를 넘겨준다.
        user_token = request.GET.get("code")

        # 인가코드를 이용해 토큰을 발급받는다
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        # 위에 api를 날리고 나서 응답으로 access_token이 온다. 이 토큰을 이용해 회원 정보를 조회한다.
        token_response_json = token_request.json()
        access_token = token_response_json.get("access_token")

        # kapi/kakao.com/v2/user/me 를 통해서 내정보를 조회한다. 동의한 것만 내려온다.
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        # 어떻게 오는지 한번 print로 찍어본다.
        print(profile_json)

        # 고유 id와 닉네임을 저장한다.
        id = profile_json.get("id")
        properties = profile_json.get("properties")
        nickname = properties.get('nickname')

        # 넘어온 고유 id가 회원가입 되어있는지 검사한다.
        user_in_db = User.objects.filter(email=id).first()
        if user_in_db is None:
            # 만약 없다면 화원가입 (User테이블에 데이터 생성)
            user_in_db = User.objects.create(email=id, password=id, nickname=nickname, name=nickname, profile_image='')

        # 로그인
        request.session['email'] = user_in_db.email
        request.session['login_check'] = True
        return render(request, 'learningspoons/main.html')

