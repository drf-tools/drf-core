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
    VERTICAL,
    HORIZONTAL,
)

# ==============================================================================
# BaseModelAdmin
# ==============================================================================
class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 20
