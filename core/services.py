from django.http import HttpRequest
from .models import ( 
    Member, MemberFamily, MemberBusiness, MemberProperty, Country,
      County, District, Occupation, Position, Relationship, BusinessType
    )
from django.db.models import Q



def createMemberService(request: HttpRequest, is_head: bool = False) -> Member:
    
    member = exactMemberData(request)

    if member == None:
        return None

    if is_head:
        member.is_head = True
    
    serial = gen_serial(member=member)
    member.serial = serial

    member.save()
    return member



#231M01D010001

# member utility function

def gen_serial(member: Member) -> str:
    try:
        last_member = Member.objects.filter(
            Q(county=member.county) & 
            Q(district=member.district)
        ).latest("created_at")
    except:
        last_member = False

    if last_member:

        latest_serial: str = last_member.serial
        latest_serial = latest_serial[9:]
        new_serial: int = int(latest_serial) + 1
        l = len(str(new_serial))
        if l >= 4:
            new_serial = f'231{member.county.code}{member.district.code}{new_serial}'
        elif l == 3:
            new_serial = f'231{member.county.code}{member.district.code}0{new_serial}'
        elif l == 2:
            new_serial = f'231{member.county.code}{member.district.code}00{new_serial}'
        else:
            new_serial = f'231{member.county.code}{member.district.code}000{new_serial}'
  
    else:
        new_serial = f'231{member.county.code}{member.district.code}0001'

    return new_serial


def exactMemberData(request: HttpRequest, member: Member = None) -> Member:

    county = County.objects.get(id=request.POST['county'])
    country = Country.objects.get(id=request.POST['country'])
    origin = Country.objects.get(id=request.POST['origin'])
    district = District.objects.get(id=request.POST['district'])
    occupation = Occupation.objects.get(id=request.POST['occupation'])
    position = Position.objects.get(id=request.POST['position'])
    
    image = request.FILES.get('image')
    number = request.POST['number']
    middlename = request.POST['middlename']
    email = request.POST['email']
    address = request.POST['address']
    place_id = request.POST['place_id']
    comment = request.POST['comment']
    firstname = request.POST['firstname']


    if member:
        member.firstname = firstname
        member.lastname = request.POST['lastname']
        member.community = request.POST['community']
        member.city = request.POST['city']
        member.statue = request.POST['statue']
        member.country.pk = country.pk
        member.county.pk = county.pk
        member.occupation.pk =occupation.pk
        member.district.pk = district.pk
        member.origin.pk = origin.pk
        member.gender = request.POST['gender']
        member.position.pk = position.pk
        member.birth_date = request.POST['birth_date']
    else:
        member = Member(
            firstname = firstname,
            lastname = request.POST['lastname'],
            community = request.POST['community'],
            city = request.POST['city'],
            statue = request.POST['statue'],
            country = country,
            county = county,
            occupation =occupation,
            district = district,
            origin = origin,
            gender = request.POST['gender'],
            position = position,
            birth_date = request.POST['birth_date']
        )
        
    if email != None:
        member.email = email

    if place_id != None:
        member.place_id = place_id

    if address != None:
        member.address = address

    if number != None:
        member.number = number
    
    if middlename != None:
        member.middlename = middlename
    
    if image != None:
        member.image = image

    if comment != None:
        member.comment = comment

    print(member.firstname)

    return member



def exactMemberBusinessData(request: HttpRequest, business: MemberBusiness = None) -> MemberBusiness:
    try:
        member = getmember(request.POST['member'])
        place_id = request.POST['place_id']
        type = BusinessType.objects.get(pk=request.POST['type'])
        address = request.POST['address']
        description = request.POST['description']

        
        if member:
            if business:
                business.member = member
                business.name = request.POST['name']
                business.type = type
            else:
                business = MemberBusiness(
                    member = member,
                    name = request.POST['name'],
                    type = type,

                )
            if place_id != None:
                business.place_id = place_id

            if description != None:
                business.description = description

            if address != None:
                business.address = address
            return business
    except:
        return None
    

def exactMemberPropertyData(request: HttpRequest, property: MemberProperty = None) -> MemberProperty:
    try:
        member = getmember(int(request.POST['member']))
        place_id = request.POST['place_id']
        address = request.POST['address']
        description = request.POST['description']

        
        if member:
            if property:
                property.member = member
                property.name = request.POST['name']

            else:
                property = MemberProperty(
                    member = member,
                    name = request.POST['name']
                )
            if place_id != None:
                property.place_id = place_id

            if description != None:
                property.description = description

            if address != None:
                property.address = address

            return property
    except:
        return None
    


def getMemberDepService():
    county = County.objects.all()
    country = Country.objects.all()
    district = District.objects.all()
    occupation = Occupation.objects.all()
    position = Position.objects.all()

    util = {'country': country, 'county': county, 
            'district': district, 'occupation': occupation,
            'position': position }
    
    return util


def getMemberDepExService(model, ex):
    
    util = getMemberDepService()
    util[ex] = model.objects.all()
    
    return util
    

# ///utility function end //
       
def updateMember(member: Member, request: HttpRequest) -> Member:

    data = exactMemberData(request=request, member=member)

    if data is None:
        return None
    
    data.save()

    return member


def deleteMember(id: int) -> bool:
    member = getmember(id)
    if member:
        member.delete()

        return True
    return False


def listMember():
    members = Member.objects.all( 
        ).select_related('district', 'county', 'origin',
                        'country', 'occupation', 'position').order_by('created_at')
    
    return members


def getmember(id: int) -> Member:
    member = Member.objects.filter(
        pk=id).select_related('district', 'county', 'origin',
                              'country', 'occupation', 'position').first()
    if member:
        return member 
    
    return None

def getmemberBySerial(id: str) -> Member:
    member = Member.objects.filter(
        serial=id).select_related('district', 'county', 'origin',
                              'country', 'occupation', 'position').first()
    return member 




# MemberFimalyService

def createMemberFamilyService(request: HttpRequest) -> MemberFamily:

    try:
        member = createMemberService(request=request)
        relationship = Relationship.objects.get(id=request.POST['relationship'])
        head = getmember(int(request.POST['head']))

        if member:
            memberFamily = MemberFamily(
                member = member,
                head = head,
                relationship = relationship
            )
            memberFamily.save()

            return memberFamily
    except:
        return None
    

def updateMemberFamilyService(id: int, request: HttpRequest) -> MemberFamily:

    member = getMemberFamily(id)

    if member is None:
        return None
    
    member1 = updateMember(id=member.member.pk, request=request)

    if member1 is None:
        return None

    member.member = member1
    member.relationship = Relationship.objects.get(id=request.POST['relationship'])
    member.head = getmember(int(request.POST['head']))

    member.save()

    return member



def getMemberFamily(id) -> MemberFamily:
    try:
        member = MemberFamily.objects.get(
            pk=id)
    except:
        member = False

    if member:
        return member

    return None


def getMemberFamilyList(id):
    member = MemberFamily.objects.all().filter(
        head__pk=id).select_related('member', 'member__district', 'member__county', 'member__origin',
                              'member__country', 'member__occupation', 'member__position')
    if member:
        return member
    
    return None


def deleteMemberFamily(id: int) -> bool:
    f_member = getMemberFamily(id)
    if f_member:
        f_member.delete()
        return True
    return False



# Business Service

def createMemberBusinessService(request: HttpRequest):
    business = exactMemberBusinessData(request=request)
    if business:
        business.save()
        return business
    
    return None
    
    
def updateMemberBusinessService(id: int, request: HttpRequest) -> MemberBusiness:
    business = getMemberBusiness(id=id)
    if business:
        data = exactMemberBusinessData(request=request,business=business)

        if data is None:
            return None
        
        data.save()
    return data
        

def getMemberBusiness(id):
    try:
        business = MemberBusiness.objects.get(
            pk=id)
        if business:
            return business
        return None
    except:
       return None

    
def getMemberBusinessList(id):
    business = MemberBusiness.objects.all().filter(
        member__pk=id).select_related('member', 'member__district', 'member__county', 'member__origin',
                              'member__country', 'member__occupation', 'member__position')
    if business:
        return business
    
    return None

def deleteMemberBusiness(id: int) -> bool:
    business = getMemberBusiness(id)
    if business:
        business.delete()
        return True
    return False


# Property Service

def getMemberProperty(id) -> MemberProperty:
    try:
        property = MemberProperty.objects.get(
            pk=id)
        if property:
            return property
        return None
    except:
       return None

def getMemberPropertyList(id):
    object = MemberProperty.objects.all().filter(
        member__pk=id).select_related('member', 'member__district', 'member__county', 'member__origin',
                              'member__country', 'member__occupation', 'member__position')
    if object:
        return object
    
    return None


def createMemberPropertyService(request: HttpRequest) -> MemberProperty:

    property = exactMemberPropertyData(request=request)
    property.save()

    return property

def updateMemberPropertyService(id: int, request: HttpRequest) -> MemberProperty:
    property = getMemberProperty(id=id)

    if property:
        data = exactMemberPropertyData(request=request, property=property)
        if data is None:
            return None
        data.save()
    return data


def deleteMemberProperty(id: int) -> bool:
    property = getMemberProperty(id=id)
    if property:
        property.delete()
        return True
    return False


    

