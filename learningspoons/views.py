from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Feed, Reply
from user.models import User


class Main(APIView):
    def get(self, request):
        if request.session.get('login_check'):
            email = request.session.get('email')
            find_user = User.objects.filter(email=email).first()

            data_list = []  # 빈 리스트

            for feed in Feed.objects.all().order_by('-id'):
                # Feed.objects.all() => [피드1 + 피드1에대한 댓글, 피드2 + 피드2에대한 댓글, 피드3 ...]
                data_list.append(dict(id=feed.id,
                                      image=feed.image,
                                      profile_image=feed.profile_image,
                                      nickname=feed.nickname,
                                      content=feed.content,
                                      reply_list=Reply.objects.filter(feed_id=feed.id)  # [댓글 1, 댓글2 .... ]
                                      )
                                 )

            return render(request, 'learningspoons/main.html',
                          context=dict(
                              data_list=data_list,
                              user_info=find_user
                          ))
        else:
            return render(request, 'user/login.html')



