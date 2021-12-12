import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Feed, Reply, Like
from learningspoons.settings import MEDIA_ROOT


class Test(APIView):
    def get(self, request):
        return Response(status=200, data=dict(message="GET으로 API를 호출했습니다."))

    def post(self, request):
        print("POST 요청이 들어옴")

        file = request.FILES['file']  # 인풋에서 파일 가져오기
        client_content = request.data.get('content')  # 인풋에서 글 내용 가져오기
        profile_image = request.data.get('profile_image')  # 인풋에서 프로필 이미지 가져오기
        nickname = request.data.get('nickname')  # 인풋에서 닉네임 가져오기
        print(file, client_content, profile_image, nickname)  # 출력

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        Feed.objects.create(content=client_content, image=uuid_name, profile_image=profile_image, nickname=nickname)

        return Response(status=200, data=dict(message="POST로 API를 호출했습니다."))


class CreateReply(APIView):
    def post(self, request):
        print("POST 요청이 들어옴")

        feed_id = request.data.get('feed_id')  # 인풋에서 글 내용 가져오기
        content = request.data.get('content')  # 인풋에서 프로필 이미지 가져오기
        nickname = request.data.get('nickname')  # 인풋에서 닉네임 가져오기

        Reply.objects.create(content=content, feed_id=feed_id, nickname=nickname)

        return Response(status=200, data=dict(message="댓글 쓰기 성공"))


class CreateLike(APIView):
    def post(self, request):
        print("POST 요청이 들어옴")

        feed_id = request.data.get('feed_id')  # 인풋에서 글 내용 가져오기
        email = request.data.get('email')  # 인풋에서 닉네임 가져오기

        Like.objects.create(feed_id=feed_id, email=email)

        return Response(status=200, data=dict(message="좋아요 성공"))


class CancelLike(APIView):
    def post(self, request):
        print("POST 요청이 들어옴")

        feed_id = request.data.get('feed_id')  # 인풋에서 글 내용 가져오기
        email = request.data.get('email')  # 인풋에서 닉네임 가져오기

        find_like = Like.objects.filter(feed_id=feed_id, email=email).first()
        # 좋아요1

        find_like.delete()

        return Response(status=200, data=dict(message="좋아요취소 성공"))
