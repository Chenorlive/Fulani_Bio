from django.contrib import admin
from .models import ( 
    Member, MemberFamily, MemberBusiness, MemberProperty,
    BusinessType, Position, PropertyImage, Country, County,
    Relationship, District, Occupation,              
)

# Register your models here.

admin.site.register(Member)

admin.site.register(MemberBusiness)

admin.site.register(MemberFamily)

admin.site.register(MemberProperty)

admin.site.register(BusinessType)

admin.site.register(Position)

admin.site.register(PropertyImage)

admin.site.register(Country)

admin.site.register(County)

admin.site.register(Relationship)

admin.site.register(District)

admin.site.register(Occupation)
