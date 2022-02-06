"""learningspoons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from content.views import Test, CreateReply, CreateLike, CancelLike, CreateProduct, ProductDetail, CartView, AddCart, \
    PayCart, ClearCart, CreateReview, AddProduct
from learningspoons import settings
from learningspoons.views import Main, Search
from user.views import Join, Login, KakaoLogin, KakaoCallBack, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('main/', Main.as_view()),
    path('', Main.as_view(), name='main'),
    path('search/', Search.as_view(), name='search'),
    path('test', Test.as_view(), name='test'),
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
    path('reply/', CreateReply.as_view(), name='reply'),
    path('like/', CreateLike.as_view(), name='like'),
    path('cancellike/', CancelLike.as_view(), name='cancellike'),
    path('kakaologin/', KakaoLogin.as_view(), name='kakaologin'),
    path('kakao/oauth', KakaoCallBack.as_view(), name='oauth'),
    path('createproduct/', CreateProduct.as_view(), name='createproduct'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('addcart/', AddCart.as_view(), name='addcart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('paycart/', PayCart.as_view(), name='pay_cart'),
    path('clearcart/', ClearCart.as_view(), name='clear_cart'),
    path('logout/', Logout.as_view(), name='logout'),
    path('review/', CreateReview.as_view(), name='review'),
    path('addproduct/', AddProduct.as_view(), name='addproduct')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
