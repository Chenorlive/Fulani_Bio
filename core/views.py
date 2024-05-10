from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.db.models import Q

from core.services import ( 
    createMemberBusinessService, createMemberFamilyService, createMemberService, getMemberBusiness, 
    getMemberBusinessList, getMemberDepService, getMemberFamily, getMemberFamilyList, 
    getMemberPropertyList, getmember, listMember, updateMember, updateMemberBusinessService, 
    updateMemberFamilyService, createMemberPropertyService,
    getmemberBySerial, getMemberProperty, updateMemberPropertyService
)
from .models import (BusinessType, Member, MemberFamily, Relationship)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


@login_required
def index(request):

    min_year = datetime.now() - timedelta(days=6570)
    
    men = len(Member.objects.filter(
            Q(gender='Male') & Q(birth_date__lte=min_year.date())
        )
    )

    women = len(Member.objects.filter(
            Q(gender='Female') & Q(birth_date__lte=min_year.date())
        )
    )

    boy = len(Member.objects.filter(
            Q(gender='Male') & Q(birth_date__gte=min_year.date())
        )
    )

    girl = len(Member.objects.filter(
            Q(gender='Female') & Q(birth_date__gte=min_year.date())
        )
    )

    context = {'men': men, 'women': women, 'boy': boy, 'girl': girl}

    return render(request, 'index.html', context)


# member

class MemberListView(LoginRequiredMixin, generic.ListView):
    queryset = listMember()
    model = Member
    paginate_by = 30
    context_object_name = 'object'
    extra_context = {'year': datetime.now().year, 'title': 'Home'}
    template_name = 'member/member_list.html'


class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    template_name = 'member/member_detail.html'
    context_object_name = 'object'
    slug_field = 'serial'
    slug_url_kwarg = 'serial'

    def get_context_data(self, **kwargs):
        member = getmemberBySerial(self.kwargs['serial'])
        family_member = getMemberFamilyList(member.pk)
        business = getMemberBusinessList(member.pk)
        member_property = getMemberPropertyList(member.pk)

        context = super().get_context_data(**kwargs)
        context['familyMember'] = family_member
        context['business'] = business
        context['member_property'] = member_property
        return context

    extra_context = {'year': datetime.now().year, 'title': 'User List'}

    def get_queryset(self):
        return listMember()



@login_required
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member Successful Deleted')
        return redirect('/')
    return render(request, 'member/member_delete.html', {'object': member})



class SearchMemberListView(generic.ListView):
    model = Member
    template_name = 'member/member_list.html'

    context_object_name = 'object'
    extra_context = {'year': datetime.now().year, 'title': 'Member List'}


    def get_queryset(self):
        member = Member.objects.all().filter(
            Q(email__icontains=self.request.GET['query']) |
            Q(firstname__icontains=self.request.GET['query']) |
            Q(lastname__icontains=self.request.GET['query']) |
            Q(city__icontains=self.request.GET['query'])
        )
        return member



def createMember(request):
    util = getMemberDepService()

    if request.method == 'POST':
        member = createMemberService(request=request, is_head=True)
        if member:
            messages.success(request, 'Member created successful')
            return redirect('home')

    return render (request, 'member/member_create.html', {'util': util})



def updateMemberView(request, pk):
    util = getMemberDepService()

    member = getmember(id=pk)

    if request.method == 'POST':
        member1 = updateMember(id=pk, request=request)

        if member1:
            messages.success(request, 'Member updated successful')
            return redirect('home')

    return render (request, 'member/member_update.html', {'util': util, 'object': member})


# Family 

def createMemberFamilyView(request, pk):
    util = getMemberDepService()
    head = getmember(pk)
    relationship = Relationship.objects.all()

    if request.method == 'POST':
        member = createMemberFamilyService(request=request)

        if not member:
            messages.error(request, 'Family Member creation Fail')
            return redirect('')
        
        messages.success(request, 'Family Member was created successful')
        return redirect('home')
    return render (request, 'family/memberFamily_create.html', 
                   {'util': util, 'head': head, 'relationship': relationship })



def updateMemberFamilyView(request, pk):
    util = getMemberDepService()
    f_member = getMemberFamily(pk)

    if request.method == 'POST':
        member = updateMemberFamilyService(request=request)

        if not member:
            messages.error(request, 'Member creation Fail')
            return redirect('new_member')
        
        messages.success(request, 'Family Member was created successful')
        return redirect('home')
    return render (request, 'family/memberFamily_create.html', 
                   {'util': util, 'object': f_member})




# Business 

def createMemberBusinessView(request, pk):
    member = getmember(pk)
    business_type = BusinessType.objects.all()

    if request.method == 'POST':
        business = createMemberBusinessService(request=request)

        if not business:
            messages.error(request, 'Business creation Fail')
            return redirect(f'/member/{member.serial}/')
        
        messages.success(request, 'Family Member was created successful')
        return redirect(f'/member/{member.serial}/')
    return render (request, 'business/business_create.html', {'business_type': business_type, 'member': member})


def updateMemberBusinessView(request, pk):
    business_type = BusinessType.objects.all()
    business = getMemberBusiness(pk)

    if request.method == 'POST':
        business = updateMemberBusinessService(request=request, id=pk)

        if not business:
            messages.error(request, 'Business updated fail')
            return redirect(f'/member/list/')
        
        messages.success(request, 'Business updated successful')
        return redirect(f'/member/{business.member.serial}/')

    return render (request, 'business/business_update.html', 
                   {'object': business, 'business_type': business_type})



# Property

def createMemberPropertyView(request, pk):
    member = getmember(pk)

    if request.method == 'POST':
        property = createMemberPropertyService(request=request)

        if not property:
            messages.error(request, 'Member Property creation Fail')
            return redirect(f'/member/{member.serial}/')
        
        messages.success(request, 'Member Property was created successful')
        return redirect(f'/member/{member.serial}/')
    return render (request, 'property/property_create.html', {'member': member})



def updateMemberPropertyView(request, pk):
    property = getMemberProperty(pk)

    if request.method == 'POST':
        property = updateMemberPropertyService(request=request, id=pk)

        if not property:
            messages.error(request, 'Business updated fail')
            return redirect(f'/member/list/')
        
        messages.success(request, 'Business updated successful')
        return redirect(f'/member/{property.member.serial}/')

    return render (request, 'property/property_update.html', 
                   {'object': property })



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'you have successful login')
            return redirect('home')
        messages.error(request, 'email or password wrong')
        return redirect('login')
    return render(request, 'login.html', 
                  {'year': datetime.now().year, 'title': 'Login'})



def logout_view(request):
    logout(request)
    return redirect('login')



