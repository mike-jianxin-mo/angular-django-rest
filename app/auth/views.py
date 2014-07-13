from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from app.sub_site.serializers import SubSiteSerializer
from app.sub_site.models import SubSite
from .serializers import UserSerializer
import base64

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSubSiteList(generics.ListAPIView):
    model = SubSite
    serializer_class = SubSiteSerializer
    def get_queryset(self):
        queryset = super(UserSubSiteList, self).get_queryset()
        return queryset.filter(owner__pk=self.kwargs.get('pk'))

class AuthView(APIView):
    # authentication_classes = (authentication.QuietBasicAuthentication,)
    serializer_class = UserSerializer

    def post(self, request):
        auth_data = request.META['HTTP_AUTHORIZATION'].split(' ')
        user_data = base64.b64decode(auth_data[1]).split(':')
        user = authenticate(username=user_data[0], password=user_data[1])
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'result': 'login success!', 'username' : user.username, 'userid' : user.id})

        return Response({'result': 'login failure!'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
    	logout(request)
    	return Response({'result': 'logout!'})


    	