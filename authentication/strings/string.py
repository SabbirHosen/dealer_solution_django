from django.utils.translation import gettext as _


SET_ROLE_CHOICES = (
    ("DE", _("ডিলার")),
    ("RE", _("রিটেইলার")),
    ("DRE", _("ডাইরেক্ট রিটেইলার")),
    ("DSR", _("ডেলিভারি সেলস রিপ্রেজেন্টেটিভ")),
    ("SR", _("সেলস রিপ্রেজেন্টেটিভ")),
    ("CS", _("কাস্টমার")),
    ("AD", _("এডমিন")),
)


SET_HELP_SUPPORT_STATUS = (("PR", _("প্রসেসিং")), ("DN", _("সম্পন্ন")))
