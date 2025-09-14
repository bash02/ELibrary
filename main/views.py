from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Permission, Group
from .models import EBook, Resource, EJournal, Newspaper, BorrowBook, IDCard, Category, Subject, User
from .serializers import UserSerializer, EBookSerializer, ResourceSerializer, EJournalSerializer, NewspaperSerializer, BorrowBookSerializer, IDCardSerializer, CategorySerializer, SubjectSerializer, PermissionSerializer, GroupSerializer
from .permissions import CustomAdminPermission

class EbookViewSet(viewsets.ModelViewSet):
    serializer_class = EBookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []  # Allow any user (including anonymous) to read
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return EBook.objects.all().order_by('-created_at')
        return EBook.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Admin-only approval."""
        project = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to make approvement"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.approved = True
        project.save()
        return Response({"detail": "Project approved successfully."})


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Resource.objects.all().order_by('-created_at')
        return Resource.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Admin-only approval."""
        project = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to make approvement"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.approved = True
        project.save()
        return Response({"detail": "Project approved successfully."})


class EJournalViewSet(viewsets.ModelViewSet):
    serializer_class = EJournalSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return EJournal.objects.all().order_by('-created_at')
        return EJournal.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Admin-only approval."""
        project = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to make approvement"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.approved = True
        project.save()
        return Response({"detail": "Project approved successfully."})


class NewspaperViewSet(viewsets.ModelViewSet):
    serializer_class = NewspaperSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Newspaper.objects.all().order_by('-created_at')
        return Newspaper.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Admin-only approval."""
        project = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to make approvement"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.approved = True
        project.save()
        return Response({"detail": "Project approved successfully."})


class BorrowBookViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins see all, users see only their records
        user = self.request.user
        if user.is_staff:
            return BorrowBook.objects.all()
        return BorrowBook.objects.filter(user=user)


class IDCardViewSet(viewsets.ModelViewSet):
    serializer_class = IDCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return IDCard.objects.all()  # Admins can see all
        return IDCard.objects.filter(user=user)  # Users can only see their own ID card

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []  # Allow any user (including anonymous) to read
        return [IsAdminUser()]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []  # Allow any user (including anonymous) to read
        return [IsAdminUser()]

class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]   # only admin users can manage groups


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

