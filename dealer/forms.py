from django import forms
from django.core.exceptions import ValidationError

from authentication.models import CustomUser, UserInformation
from django.utils.translation import gettext as _
from phonenumber_field.widgets import RegionalPhoneNumberWidget, PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from authentication.strings.string import SET_ROLE_CHOICES
from phonenumber_field.phonenumber import PhoneNumber


class DSRUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone", "first_name", "last_name", "email", "password"]
        labels = {
            "phone": _("মোবাইল"),
            "first_name": _("প্রথম নাম"),
            "last_name": _("শেষ নাম"),
            "email": _("ইমেইল"),
            "password": _("পাসওয়ার্ড"),
        }
        widgets = {
            "phone": PhoneNumberPrefixWidget(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                },
                country_choices=[("BD", "Bangladesh"),],
                initial="BD",
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
        }

    def save(self, commit=True):
        user = super(DSRUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class DSRUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "shop_name": _("দোকানের নাম"),
            "shop_address": _("দোকানের ঠিকানা"),
            "photo": _("নিজের ছবি"),
            "shop_photo": _("দোকানের ছবি"),
            "nid_number": _("জাতীয় পরিচয় পত্র নাম্বার"),
            "trade_licence": _("ট্রেড লাইসেন্স নাম্বার"),
        }
        widgets = {
            "shop_name": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "shop_address": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "photo": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "capture": "camera",
                    "onchange": "updateFileName(this)",
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2",
                }
            ),
            "shop_photo": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "capture": "camera",
                    "onchange": "updateFileName(this)",
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2",
                }
            ),
            "nid_number": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
            "trade_licence": forms.TextInput(
                attrs={
                    "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900 focus:border-2"
                }
            ),
        }


class CollectionForm(forms.Form):
    prevDue = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
                "readonly": "readonly",
            }
        ),
        label="মোট বকেয়া",
    )
    totalDeposit = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900"
            }
        ),
        label="মোট জমা",
    )
    totalDue = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
                "readonly": "readonly",
            }
        ),
        label="মোট বাকি",
    )

    def clean(self):
        cleaned_data = super().clean()
        prev_due = cleaned_data.get("prevDue")
        total_deposit = cleaned_data.get("totalDeposit")
        if total_deposit <= 0:
            raise ValidationError("জমা টাকা সঠিক দিন", code="invalid_due_amount")

        # Perform your custom validation
        if (
            prev_due is not None
            and total_deposit is not None
            and prev_due - total_deposit < 0
        ):
            raise ValidationError(
                "মোট বকেয়া কম হতে পারে না জমার চেয়ে", code="invalid_due_amount"
            )

        return cleaned_data


class DSRIndividualCollectionForm(forms.Form):
    total_bill = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
                "readonly": "readonly",
            }
        ),
        label="আজকের বিল",
    )
    discount = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900"
            }
        ),
        label="ডিস্কাঊন্ট",
    )
    net_bill = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
                "readonly": "readonly",
            }
        ),
        label="মোট বিল",
    )
    totalDeposit = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
            }
        ),
        label="জমা",
    )
    totalDue = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full bg-[#F6F9FC] focus:outline-none focus:shadow-outline border-[1.5px] border-gray-400 rounded py-3 px-3 block appearance-none leading-normal focus:border-gray-900",
                "readonly": "readonly",
            }
        ),
        label="বাকি",
    )

    def clean(self):
        cleaned_data = super().clean()
        total_bill = cleaned_data.get("total_bill")
        discount = cleaned_data.get("discount")
        deposit = cleaned_data.get("totalDeposit")
        net_bill = cleaned_data.get("net_bill")

        if deposit <= 0:
            raise ValidationError("জমা টাকা সঠিক দিন", code="invalid_due_amount")
        #
        # # Perform your custom validation
        if net_bill is not None and deposit is not None and net_bill - deposit < 0:
            raise ValidationError(
                "মোট বিলের চেয়ে জমা বেশি হতে পারে না", code="invalid_due_amount"
            )
        if (
            total_bill is not None
            and discount is not None
            and total_bill - discount < 0
        ):
            raise ValidationError(
                "ডিস্কাউন্টের পরিমান আজকের বিলের থেকে বেশি হতে পারে না",
                code="invalid_discount_amount",
            )
        return cleaned_data
