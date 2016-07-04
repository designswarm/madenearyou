import phonenumbers
from ukpostcodeutils import validation

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_uk_postcode(value):
    if validation.is_valid_postcode(value) is False:
        raise ValidationError(
            _('%(value)s is not a valid postcode'),
            params={'value': value},
        )

def validate_uk_phone_number(value):
    num = phonenumbers.parse(value, 'GB')

    try:
        if phonenumbers.is_valid_number(num) is False:
            raise ValidationError(
                _('%(value)s is not a valid UK phone number'),
                params={'value': value},
            )
    except phonenumbers.NumberParseException as e:
        raise ValidationError(
            _(str(e)),
            params={'value': value},
        )


