from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.utils.translation import gettext as _
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from phonenumber_field.formfields import PhoneNumberField


class UserLogin(forms.Form):
    phone = PhoneNumberField(widget=RegionalPhoneNumberWidget(),
                             label=_('মোবাইল'),
                             )
    password = forms.CharField(widget=forms.PasswordInput(),
                               label=_('পাসওয়ার্ড'),
                               )
    # class Meta:
    #     # model = CustomUser
    #     # fields = ['phone', 'password']
    #     labels = {
    #         'phone': _('মোবাইল'),
    #         'password': _('পাসওয়ার্ড'),
    #     }
    #     widgets = {
    #         'phone': RegionalPhoneNumberWidget(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 '
    #                                                            'sm:text-sm rounded-lg focus:ring-blue-600 '
    #                                                            'focus:border-blue-600 block w-full p-2.5 font-medium '
    #                                                            '[appearance:textfield] ['
    #                                                            '&::-webkit-outer-spin-button]:appearance-none ['
    #                                                            '&::-webkit-inner-spin-button]:appearance-none'}),
    #         'password': forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 '
    #                                                         'sm:text-sm rounded-lg focus:ring-blue-600 '
    #                                                         'focus:border-blue-600 block w-full p-2.5 font-medium'}),
    #     }
