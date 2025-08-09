from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def create_account(request):
    try:
        serializer = CustomUserSerializer(data=request.data)
        if not request.data.get("role"):
            return Response(
                {"status": "Error", "message": "Role field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            CustomUser.objects.create_user(**serializer.validated_data)
            user_data = serializer.data
            user_data.pop("password")
            return Response(
                {"status": "Success", "data": user_data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "Error", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"status": "Error", "data": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"status": "Success", "message": "User is logged out"})
    except Exception as e:
        return Response(
            {"status": "Error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
