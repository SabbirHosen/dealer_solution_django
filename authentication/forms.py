from django import forms
from .models import CustomUser, UserInformation
from django.utils.translation import gettext as _
from phonenumber_field.widgets import RegionalPhoneNumberWidget, PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from .strings.string import SET_ROLE_CHOICES
from phonenumber_field.phonenumber import PhoneNumber


class UserLogin(forms.Form):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'bg-gray-50 border border-gray-300 '
                                                                              'text-gray-900 sm:text-sm rounded-lg '
                                                                              'focus:ring-blue-600 '
                                                                              'focus:border-blue-600 block w-full '
                                                                              'p-2.5 font-medium ['
                                                                              'appearance:textfield] ['
                                                                              '&::-webkit-outer-spin-button'
                                                                              ']:appearance-none ['
                                                                              '&::-webkit-inner-spin-button'
                                                                              ']:appearance-none',
                                                                     'placeholder': "+8801000000000"},
                                                            country_choices=[
                                                                ("BD", "Bangladesh"),
                                                            ],
                                                            initial='BD',
                                                            ),
                             label=_('মোবাইল'),
                             required=True,
                             region='BD'
                             )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 '
                                                                          'text-gray-900 sm:text-sm rounded-lg '
                                                                          'focus:ring-blue-600 focus:border-blue-600 '
                                                                          'block w-full p-2.5 font-medium',
                                                                 "placeholder": "••••••••"}),
                               label=_('পাসওয়ার্ড'),
                               required=True
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
    user_role = forms.ChoiceField(choices=SET_ROLE_CHOICES,
                                  required=True,
                                  label=_('ব্যবহারকারীর ভূমিকা'),
                                  widget=forms.Select(attrs={'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}))

    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'phone': _('মোবাইল'),
            'first_name': _('প্রথম নাম'),
            'last_name': _('শেষ নাম'),
            'email': _('ইমেইল'),
            'password': _('পাসওয়ার্ড')
        }
        widgets = {
            'phone': PhoneNumberPrefixWidget(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'},
                            country_choices=[
                                ("BD", "Bangladesh"),
                            ],
                            initial='BD'),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),

        }

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
        labels = {
            'shop_name': _('দোকানের নাম'),
            'shop_address': _('দোকানের ঠিকানা'),
            'photo': _('নিজের ছবি'),
            'shop_photo': _('দোকানের ছবি'),
            'nid_number': _('জাতীয় পরিচয় পত্র নাম্বার'),
            'trade_licence': _('ট্রেড লাইসেন্স নাম্বার')
        }
        widgets = {
            'shop_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'shop_address': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'photo': forms.FileInput(
                attrs={'accept': "image/*", "capture": "camera", "onchange": "updateFileName(this)",
                       'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'shop_photo': forms.FileInput(
                attrs={'accept': "image/*", "capture": "camera", "onchange": "updateFileName(this)",
                       'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'nid_number': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'trade_licence': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _('প্রথম নাম'),
            'last_name': _('শেষ নাম'),
            'email': _('ইমেইল'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2'}),
        }


class PinChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 font-medium [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none', 'placeholder': '****'}
    ),
        label=_('পুরাতন পাসওয়ার্ড'),
        required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 font-medium', 'placeholder': '****'}
    ),
        label=_('নতুন পাসওয়ার্ড'),
        required=True)

    retype_new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 font-medium', 'placeholder': '****'}
    ),
        label=_('আবার নতুন পাসওয়ার্ড'),
        required=True)
