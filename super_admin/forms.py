from django import forms
from django.utils.translation import gettext as _
from .models import HelpSupport


class HelpSupportFormUser(forms.ModelForm):
    class Meta:
        model = HelpSupport
        fields = ['problems']
        labels = {
            'problems': _('সমস্যা'),
        }
        widgets = {
            'problems': forms.Textarea(
                attrs={'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2',
                       'placeholder': "সংক্ষেপে সমস্যা সম্পর্কে লিখুন",
                       },
            )
        }
