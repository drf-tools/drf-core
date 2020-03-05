""" Provides all common fields. We prefer wrapper method instead of
    sub-classing field class to make sure our model can stay with
    pre-defined field type in django. This will help to avoid situations
    where 3rd-party component cannot handle custom field classes.
"""
from django.db.models import ( # noqa
    AutoField,
    BigAutoField,
    BigIntegerField,
    BinaryField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    EmailField,
    FileField,
    FilePathField,
    FloatField,
    ImageField,
    IntegerField,
    GenericIPAddressField,
    NullBooleanField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SlugField,
    SmallIntegerField,
    TextField,
    TimeField,
    URLField,
    UUIDField,
    ForeignKey,
    ManyToManyField,
    OneToOneField,
    Sum,
    Value,
    When,
    Case,
    F,
    Count,
)

from django_extensions.db.models import ( # noqa
    AutoSlugField,
)

# from django_countries.fields import CountryField # noqa


# =============================================================================

NAME_MAX_LENGTH = 100
LONG_NAME_MAX_LENGTH = 250
SHORT_NAME_MAX_LENGTH = 30


class NameField(CharField):
    """ This function provide a unique name field.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', False)
        kwargs.setdefault('blank', False)
        kwargs.setdefault('null', False)
        kwargs.setdefault('max_length', NAME_MAX_LENGTH)

        super(NameField, self).__init__(*args, **kwargs)


class LongNameField(CharField):
    """ This function provide a unique name field.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', False)
        kwargs.setdefault('blank', False)
        kwargs.setdefault('null', False)
        kwargs.setdefault('max_length', LONG_NAME_MAX_LENGTH)

        super(LongNameField, self).__init__(*args, **kwargs)


class ShortNameField(CharField):
    """ This function provide a unique name field.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', False)
        kwargs.setdefault('blank', False)
        kwargs.setdefault('null', False)
        kwargs.setdefault('max_length', SHORT_NAME_MAX_LENGTH)

        super(ShortNameField, self).__init__(*args, **kwargs)


class NullShortNameField(CharField):
    """ This function provide a unique name field.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('null', True)
        kwargs.setdefault('max_length', SHORT_NAME_MAX_LENGTH)

        super(NullShortNameField, self).__init__(*args, **kwargs)


# =============================================================================

class NameSlugField(AutoSlugField):
    """ We often create auto slug from name field. This function
        provides common way for creating such auto name slug.
    """

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs.setdefault('unique', False)
        kwargs.setdefault('max_length', NAME_MAX_LENGTH)
        kwargs.setdefault('populate_from', 'name')

        super(NameSlugField, self).__init__(*args, **kwargs)


class LongNameSlugField(AutoSlugField):
    """ We often create auto slug from name field. This function
        provides common way for creating such auto name slug.
    """

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs.setdefault('max_length', LONG_NAME_MAX_LENGTH)
        kwargs.setdefault('populate_from', 'name')

        super(LongNameSlugField, self).__init__(*args, **kwargs)


class ShortNameSlugField(AutoSlugField):
    """ We often create auto slug from name field. This function
        provides common way for creating such auto name slug.
    """

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs.setdefault('max_length', SHORT_NAME_MAX_LENGTH)
        kwargs.setdefault('populate_from', 'name')

        super(ShortNameSlugField, self).__init__(*args, **kwargs)


# =============================================================================

DESC_MAX_LENGTH = 250
SHORT_DESC_MAX_LENGTH = 100
LONG_DESC_MAX_LENGTH = 1000


class DescField(CharField):
    """ A field that stores a normal description text """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', DESC_MAX_LENGTH)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', '')
        kwargs.setdefault('verbose_name', 'Description')

        super(DescField, self).__init__(*args, **kwargs)


class LongDescField(CharField):
    """ A field that stores a long description text """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', LONG_DESC_MAX_LENGTH)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', '')
        kwargs.setdefault('verbose_name', 'Description')

        super(LongDescField, self).__init__(*args, **kwargs)


class ShortDescField(CharField):
    """ A field that stores a short description text """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', SHORT_DESC_MAX_LENGTH)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', '')
        kwargs.setdefault('verbose_name', 'Description')

        super(ShortDescField, self).__init__(*args, **kwargs)


# =============================================================================

class CodeField(CharField):
    """ In the company, we use code a lot. The code should be
        a single word that can be used as a directory name,
        email name, etc. The code should be unique across the
        whole's company universe.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        kwargs['unique'] = True
        super(CodeField, self).__init__(*args, **kwargs)


class MoneyField(DecimalField):
    """ All currency values should utilize DecimalField over FloatField
        http://docs.python.org/library/decimal.html
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 20)
        kwargs.setdefault('decimal_places', 2)

        super(MoneyField, self).__init__(*args, **kwargs)


class PercentageField(DecimalField):
    """ A field for storing percentage.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 6)
        kwargs.setdefault('decimal_places', 2)

        super(PercentageField, self).__init__(*args, **kwargs)


class PhoneNumberField(CharField):
    """ A field for storing phone number.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', False)

        super(PhoneNumberField, self).__init__(*args, **kwargs)


class SocialUsernameField(CharField):
    """ A field for storing social username, such as skype's username,
        github's username, etc.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', False)

        super(SocialUsernameField, self).__init__(*args, **kwargs)


class SkypeUsernameField(SocialUsernameField):
    pass


class HomepageUrlField(URLField):
    """ A field for storing facebook handle.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', False)

        super(HomepageUrlField, self).__init__(*args, **kwargs)


# =============================================================================

class ListOrderField(IntegerField):
    """ This defines a field for ui display list ordering. """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', False)
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('default', 0)

        super().__init__(*args, **kwargs)


class NullFloatField(FloatField):
    """A nullable float field"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)

        super().__init__(*args, **kwargs)


# =============================================================================

class NullDateTimeField(DateTimeField):
    """ A nullable DateTimeField
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('null', True)
        super().__init__(*args, **kwargs)


class NullDecimalField(DecimalField):
    """ A nullable DecimalField
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super().__init__(*args, **kwargs)
