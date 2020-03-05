from django.conf import settings

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_core.pagination import BasePagination
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import (
    action,
    permission_classes,
    authentication_classes
)


class PaginationViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination


class FilteringViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = '__all__'


class AuthenticationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (SessionAuthentication, TokenAuthentication)


class CommonViewSet:
    def create_response(self, data=None):
        return Response(data=data, status=status.HTTP_200_OK)

    def bad_request(self, message=None, code=None):
        """
        Return bad request with message content & code
        """
        # Build up the error content.
        response_data = {}
        if message is not None:
            response_data['message'] = message
        if code is not None:
            response_data['code'] = code
        if message is None and code is None:
            response_data = None

        return Response(
            response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def method_not_allowed(self):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def forbidden_request(self):
        return Response(
            {
                'detail': 'You do not have permission to perform this action.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    def create_response_success(self):
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )

    def create_non_content_response(self):
        return Response(
            None,
            status=status.HTTP_204_NO_CONTENT
        )

    def get_resource_uri(self):
        domain = settings.DOMAIN
        api_root = '/api/v1/'

        return '{}{}{}/'.format(domain, api_root, self.resource_name)


class BaseViewSet(CommonViewSet, PaginationViewSet, FilteringViewSet, AuthenticationViewSet):
    """
    Base viewset should be used for normal cases.
    """
    def perform_destroy(self, instance):
        """
        Override to archive the object only, not remove.
        """
        instance.archive()


class BaseEmptyViewSet(CommonViewSet, viewsets.ModelViewSet):
    """
    This viewset is designed for a resource with custom API only.
    """

    def list(self, request, **kwargs):
        return self.method_not_allowed()

    def create(self, request, **kwargs):
        return self.method_not_allowed()

    def update(self, request, **kwargs):
        return self.method_not_allowed()

    def delete(self, request, **kwargs):
        return self.method_not_allowed()


class BaseFunctionView(CommonViewSet, APIView):
    """
    BaseFunctionView
    """

    pass
