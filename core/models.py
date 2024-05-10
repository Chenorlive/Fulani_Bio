from datetime import datetime
from io import BytesIO
from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError
import qrcode
from django.core.files import File




# Base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


Marital_Statue = [
    ("Single", "Single"),
    ("Married", "Married"),
    ("Divorced", "Divorced"),
    ("Widow", "Widow"),
    ("Widower", "Widower"),
]

Gender = [
    ("Male", "Male"),
    ("Female", "Female"),
]



# dependent models (settings)

class District(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class County(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Occupation(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Position(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name



    
class Relationship(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class BusinessType(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# core models    




class Member(BaseModel):
    serial = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_head = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Profile Image', blank=True, null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    community = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    gender = models.CharField(max_length=255, choices=Gender)
    email = models.EmailField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='origin')
    statue = models.CharField(max_length=255, choices=Marital_Statue)
    comment = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    place_id = models.TextField(null=True, blank=True)
    birth_date = models.DateField()
    qr_code = models.ImageField(upload_to='Profile QR Code', blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.height > 400 and img.width > 400:
                out_put = (400, 400)
                img.thumbnail(out_put)
                img.save(self.image.path)
        
        url = f'http://localhost:8000/member/{self.serial}/'
        qr_img = qrcode.make(url)
        qr_offset = Image.new('RGB', (400, 400), 'white')
        qr_offset.paste(qr_img)
        fName = f'{self.serial}.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(name=fName, content=File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)

    @property
    def age(self) -> int:
        a = datetime.now().date() - self.birth_date 
        
        return int(a.days/365)
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'


    

class MemberFamily(BaseModel):
    head = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='head')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member')
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE,)


    def clean(self):
        if self.head.is_head != True:
            raise ValidationError("Head must be of type head")
    
    def __str__(self):
        return f'{self.head.firstname} ({self.member.firstname})'



class MemberBusiness(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(BusinessType, on_delete=models.CASCADE) 
    address = models.TextField(null=True, blank=True)
    place_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class MemberProperty(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    place_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class PropertyImage(BaseModel):
    property = models.ForeignKey(MemberProperty, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Property Image', blank=True, null=True)

    def __str__(self):
        return self.property.name
