import os
from uuid import uuid4

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Feed, Reply, Like, Product, Cart
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


class CreateProduct(APIView):
    def post(self, request):
        file = request.FILES['file']  # 인풋에서 파일 가져오기
        seller = request.data.get('seller')  # 인풋에서 글 내용 가져오기
        description = request.data.get('description')  # 인풋에서 프로필 이미지 가져오기
        price = request.data.get('price')  # 인풋에서 닉네임 가져오기

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        Product.objects.create(description=description, image=uuid_name, seller=seller, price=price)

        return Response(status=200, data=dict(message="POST로 API를 호출했습니다."))


class ProductDetail(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)

        last_view_list = request.session.get('last_view_list', [])  # 1. 세션에 저장된 최근 본 리스트를 불러옴
        last_view_list.append(pk)   # 2. 지금 조회한 상품의 번호를 최근 본 리스트에 추가함
        request.session['last_view_list'] = last_view_list  # 3. 최근 본 리스트를 세션에 저장 (업데이트)

        return render(request, 'content/productdetail.html', context=dict(product=product))


class AddCart(APIView):
    def post(self, request):
        email = request.session.get('email')    # 세션에서 email값 가져오기
        product_id = request.data.get('product_id') # 인풋에서 product_id값 가져오기

        if Cart.objects.filter(email=email, product_id=product_id).exists():
            # 만약 장바구니에 같은 상품이 있으면 더하기
            cart_in_db = Cart.objects.filter(email=email, product_id=product_id).first()
            cart_in_db.count = cart_in_db.count + 1
            cart_in_db.save()
        else:
            # 장바구니에 같은 상품이 없으면 생성
            Cart.objects.create(email=email, product_id=product_id, count=1)

        return Response(status=200)


class CartView(APIView):
    def get(self, request):
        email = request.session.get('email')    # 세션에서 email값 가져오기

        cart_item_list = Cart.objects.filter(email=email)   # 로그인한 사용자의 장바구니 아이템 전부 가져오기

        data_list = []  # 빈 리스트 생성

        for cart_item in cart_item_list:
            # 사용자의 카트 아이템들을 하나씩 보면서 상품정보를 불러옴
            product = Product.objects.get(id=cart_item.product_id)

            # data_list에 하나씩 추가
            data_list.append(dict(
                product=product,
                count=cart_item.count
            ))

        return render(request, 'content/cart.html', context=dict(data_list=data_list))


class PayCart(APIView):
    def post(self, request):
        email = request.session.get('email')    # 세션에서 email값 가져오기

        Cart.objects.filter(email=email).delete()   # 사용자의 카트 데이터 전체 지우기

        return Response(status=200)


class ClearCart(APIView):
    def post(self, request):
        email = request.session.get('email')  # 세션에서 email값 가져오기

        Cart.objects.filter(email=email).delete()   # 사용자의 카트 데이터 전체 지우기

        return Response(status=200)

