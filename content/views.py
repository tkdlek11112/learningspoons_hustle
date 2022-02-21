import os
from uuid import uuid4

import datetime
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Product, Cart, ProductReview
from learningspoons.settings import MEDIA_ROOT
from user.models import User


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
        email = request.session.get('email')
        find_user = User.objects.filter(email=email).first()

        product = Product.objects.get(id=pk)
        reviews = ProductReview.objects.filter(product_id=product.id).order_by('-id')
        is_login = request.session.get('login_check', False)

        last_view_list = request.session.get('last_view_list', [])  # 1. 세션에 저장된 최근 본 리스트를 불러옴
        last_view_list.append(pk)   # 2. 지금 조회한 상품의 번호를 최근 본 리스트에 추가함
        request.session['last_view_list'] = last_view_list  # 3. 최근 본 리스트를 세션에 저장 (업데이트)
        is_login = request.session.get('login_check', False)

        return render(request, 'content/productdetail.html',
                      context=dict(product=product, user_info=find_user, reviews=reviews, is_login=is_login))


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
        cart_total_price = 0
        for cart_item in cart_item_list:
            # 사용자의 카트 아이템들을 하나씩 보면서 상품정보를 불러옴
            product = Product.objects.get(id=cart_item.product_id)

            # data_list에 하나씩 추가
            data_list.append(dict(
                product=product,
                count=cart_item.count,
                product_total_price = product.price*cart_item.count
            ))
            cart_total_price= cart_total_price + product.price*cart_item.count
        user_in_db = User.objects.filter(email=email).first()

        return render(request, 'content/cart.html', context=dict(data_list=data_list, cart_total_price=cart_total_price))


class PayCart(APIView):
    def post(self, request):
        email = request.session.get('email')  # 세션에서 email값 가져오기

        Cart.objects.filter(email=email).delete()   # 사용자의 카트 데이터 전체 지우기

        return Response(status=200)


class ClearCart(APIView):
    def post(self, request):
        email = request.session.get('email')  # 세션에서 email값 가져오기

        Cart.objects.filter(email=email).delete()   # 사용자의 카트 데이터 전체 지우기

        return Response(status=200)


class CreateReview(APIView):
    def post(self, request):
        review = request.data.get('review')
        nickname = request.data.get('nickname')
        product_id = request.data.get('product_id')
        star = request.data.get('star')

        ProductReview.objects.create(review=review, nickname=nickname,product_id=product_id,star=star)

        return Response(status=200)


class AddProduct(APIView):
    def get(self, request):
        return render(request, 'content/addproduct.html')


class AddProductDetail(APIView):
    def post(self, request):
        file = request.FILES['file']  # 인풋에서 파일 가져오기
        seller = request.data.get('seller')  # 인풋에서 글 내용 가져오기
        description = request.data.get('description')  # 인풋에서 프로필 이미지 가져오기
        price = request.data.get('price')  # 인풋에서 닉네임 가져오기
        name = request.data.get('name')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        Product.objects.create(description=description, image=uuid_name, seller=seller, price=price, name=name)

        return Response(status=200, data=dict(message="POST로 API를 호출했습니다."))


class ClearProduct(APIView):
    def post(self, request):
        email = request.session.get('email')  # 세션에서 email값 가져오기
        product_id = request.data.get('product_id')
        Cart.objects.filter(email=email, product_id=product_id).delete()
        return Response(status=200)


        return Response(status=200)


