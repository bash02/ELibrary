from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from .models import User, EBook, Resource, EJournal, Newspaper, BorrowBook, IDCard, Category, Subject
from django.contrib.auth.models import Permission, Group

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        write_only=True,
        source="permissions"
    )

    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "permission_ids"]


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            "id", "first_name", "last_name", "username", "email", "password",
            "phone", "student_id", "faculty", "department", "student_category",

        ]


class UserSerializer(BaseUserSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(      
        many=True,
        queryset=Group.objects.all(),
        write_only=True,
        source="groups"
    )
    permissions = PermissionSerializer(source="user_permissions", many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField( 
        many=True,
        queryset=Permission.objects.all(),
        write_only=True,
        source="user_permissions"
    )

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id", "first_name", "last_name", "username", "email",
            "phone", "student_id", "faculty", "department", "student_category",
            "is_active", "is_staff", "is_superuser", "groups", "group_ids",
            "permissions", "permission_ids", "password",
        ]

class EBookSerializer(serializers.ModelSerializer):
    subject_display = serializers.CharField(source="subject.display_name", read_only=True)

    class Meta:
        model = EBook
        fields = [
            "id",
            "title",
            "author",
            "subject",
            "subject_display",
            "upload_file",
            "thumbnail",
            "created_at",
            "approved",
        ]


    def to_representation(self, instance):
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not (request.user.is_superuser):
            raise serializers.ValidationError({"detail": "You do not have permission."})
        return super().update(instance, validated_data)



class EJournalSerializer(serializers.ModelSerializer):
    subject_display = serializers.CharField(source="subject.display_name", read_only=True)

    class Meta:
        model = EJournal
        fields = [
            "id",
            "title",
            "author",
            "subject",
            "subject_display",
            'year',
            'upload_file',
            "thumbnail",
            "created_at",
            "approved",
        ]
   
    def to_representation(self, instance):
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not (request.user.is_superuser):
            raise serializers.ValidationError({"detail": "You do not have permission."})
        return super().update(instance, validated_data)


class ResourceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="category.display_name", read_only=True)

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "thumbnail",
            "url",
            "category",
            "category_display",
            "created_at",
            "updated_at",
            "approved",
        ]

    def to_representation(self, instance):
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not (request.user.is_superuser):
            raise serializers.ValidationError({"detail": "You do not have permission."})
        return super().update(instance, validated_data)




class NewspaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newspaper
        fields = [
            "id",
            "title",
            "thumbnail",
            "url",
            "created_at",
            "updated_at",
            "approved",
        ]

    def to_representation(self, instance):
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not (request.user.is_superuser):
            raise serializers.ValidationError({"detail": "You do not have permission."})
        return super().update(instance, validated_data)


class BorrowBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowBook
        fields = ['id', 'user', 'book_title', 'borrow_date', 'return_date']

class IDCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = IDCard
        fields = ['id', 'user', 'issued_date', 'expiry_date', 'id_number', 'department', 'faculty']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add custom formatted ID Card data
        card_details = instance.get_card_details()
        return {
            "name": card_details["name"],
            "department": card_details["department"],
            "faculty": card_details["faculty"],
            "issued_date": card_details["issued_date"],
            "expiry_date": card_details["expiry_date"]
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'display_name']
