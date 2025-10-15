from .serializer import UserSerializer
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    
        token, criar = Token.objects.get_or_create(user=user)
        """Quando a view é acessado por qualquer usuário, após as validações o token é gerado para o novo user"""
        return Response({
            'user_id':user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
            }, status=status.HTTP_201_CREATED)

