from django import forms
from .models import (Member, MemberFamily, MemberProperty,
                      MemberBusiness)



class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        exclude = ('created_at', 'updated_at', 'is_head')


    def __init__(self, *args, **kwargs):
        parent_id = kwargs.pop('parent_id')
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields[''].queryset = Member.objects.filter(id=parent_id)


class MemberProperty(forms.ModelForm):

    class Meta:
        model = MemberProperty
        field = ('member', 'name', 'description', 'address', 'place_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full'



