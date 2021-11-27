from uuid import uuid4
from rest_framework.response import Response
from rest_framework.views import APIView
import os

from content.models import Feed
from learningspoons.settings import MEDIA_ROOT


class Test(APIView):
    def get(self, request):
        print("GET 요청이 들어옴")
        return Response(status=200, data=dict(message="GET 호출"))

    def post(self, request):
        print("POST 요청이 들어옴")

        file = request.FILES['file']    # 인풋에서 파일 가져오기
        content = request.data.get('content')   # 인풋에서 글 내용 가져오기
        profile_image = request.data.get('profile_image')   # 인풋에서 프로필 이미지 가져오기
        nickname = request.data.get('nickname')     # 인풋에서 닉네임 가져오기
        print(file, content, profile_image, nickname)   # 출력

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        Feed.objects.create(content=content, image=uuid_name, profile_image=profile_image, nickname=nickname)

        return Response(status=200, data=dict(message="성공"))
