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

UNIT_CHOICES = (
    ("carton", _("কার্টুন")),
    ("case", _("কেস")),
    ("package", _("পলি")),
)

DEALER_REPRESENTATIVE_STATUS = (
    ('activated', _('সক্রিয়')),
    ('deactivated', _('নিষ্ক্রিয়')),
    ('requested', _('অনুরোধ')),
)