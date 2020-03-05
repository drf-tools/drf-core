from django.urls import reverse
from six.moves.urllib.parse import urlencode
from django.contrib import admin

from django.contrib.admin import ( # noqa
    site,
    ModelAdmin,
    StackedInline,
    TabularInline,
    register,
    SimpleListFilter,
    FieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter,
    VERTICAL, HORIZONTAL
)

# Just a facade imports for all admin fields available from django-admin-easy
import easy
from easy import ( # noqa
    BaseAdminField,
    SimpleAdminField,
    BooleanAdminField,
    ForeignKeyAdminField,
    LinkChangeListAdminField,
    ExternalLinkAdminField,
    TemplateAdminField,
    ImageAdminField,
    FilterAdminField,
    CacheAdminField,

    with_tags,

    # decorators
    action,
    smart,
    short,
)

# ==============================================================================
# BaseModelAdmin
# ==============================================================================
class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 20
