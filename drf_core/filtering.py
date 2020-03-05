import rest_framework_filters as filters
from drf_core.utils import get_queryset_by_order


class BaseFiltering(filters.FilterSet):

    def filter_queryset(self, queryset):
        """
        Override this to apply filtering & ordering at the same time.
        """
        queryset = super(filters.FilterSet, self).filter_queryset(queryset)
        queryset = self.filter_related_filtersets(queryset)
        ordering_by = self.data.get('ordering')
        return get_queryset_by_order(queryset=queryset,
                                     ordering_by=ordering_by)
