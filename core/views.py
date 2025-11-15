from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import User, Recipe, Rating
from .serializers import UserSerializer, RecipeSerializer, RatingSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response


# Permissions
class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'seller'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'customer'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated]  # Customers can view
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)




class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['recipe']  # allow filtering by recipe

