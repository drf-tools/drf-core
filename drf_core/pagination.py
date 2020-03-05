# Define the paginations for resources
from rest_framework import pagination
# from configs import constants


class BasePagination(pagination.LimitOffsetPagination):
    """
    Base class for pagination.
    """

    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    template = 'rest_framework/pagination/numbers.html'
