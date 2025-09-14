from django.urls import path, include
from rest_framework_nested import routers
from .views import EbookViewSet, ResourceViewSet, EJournalViewSet, NewspaperViewSet, BorrowBookViewSet, IDCardViewSet, CategoryViewSet, SubjectViewSet, PermissionView, GroupViewSet, CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='custom-user')
router.register(r'ebook', EbookViewSet, basename='ebook')
router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'ejournal', EJournalViewSet, basename='ejournals')
router.register(r'newspaper', NewspaperViewSet, basename='newspaper')
router.register(r'borrow', BorrowBookViewSet, basename='borrow')
router.register(r'idcards', IDCardViewSet, basename='idcard')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'permissions', PermissionView, basename='permission-list'),
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]
