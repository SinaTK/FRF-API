from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from permissions import AdminOrOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    '''
        Register new users
    '''
    serializer_class = RegisterSerializer
    def post(self, request):
        ser_data = RegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    '''
        Show all users data or one of them, update or delete.
    '''
    serializer_class = UserSerializer

    permission_classes = [AdminOrOwnerOrReadOnly]
    queryset = User.objects.all()

    def list(self, request):
        srz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)        
        self.check_object_permissions(request, user)
        new_data = request.data
        srz_data = UserSerializer(instance=user, data=new_data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)        
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated seccussfully.'}, status.HTTP_200_OK)
        