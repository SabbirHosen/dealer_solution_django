from django import forms
from .models import CustomUser, UserInformation
from django.utils.translation import gettext as _
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from phonenumber_field.formfields import PhoneNumberField
from .strings.string import SET_ROLE_CHOICES


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


class UserSignupForm(forms.ModelForm):
    user_role = forms.ChoiceField(choices=SET_ROLE_CHOICES, required=True)
    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = '__all__'
        exclude = ['user']
