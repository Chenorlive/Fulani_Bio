from django.urls import path
from .views import (
    index, login_view, logout_view, createMember, MemberListView,
    MemberDetailView, SearchMemberListView, createMemberFamilyView,
    delete_member, updateMemberView, createMemberBusinessView, 
    updateMemberBusinessView, createMemberPropertyView, 
    updateMemberPropertyView
)


urlpatterns = [
    path('', index, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('member/new/', createMember, name='new_member'),
    path('member/list/', MemberListView.as_view(), name='list_member'),
    path('member/search/', SearchMemberListView.as_view(), name='search_member'),
    path('member/<serial>/', MemberDetailView.as_view(), name='detail_member'),
    path('member/update/<int:pk>/', updateMemberView, name='update_member'),
    path('member/delete/<int:pk>/', delete_member, name='delete_member'),

    path('family/new/<int:pk>/', createMemberFamilyView, name='new_family'),

    path('business/new/<int:pk>/', createMemberBusinessView, name='new_business'),
    path('business/update/<int:pk>/', updateMemberBusinessView, name='update_business'),

    path('property/new/<int:pk>/', createMemberPropertyView, name='new_property'),
    path('property/update/<int:pk>/', updateMemberPropertyView, name='update_property'),


]
