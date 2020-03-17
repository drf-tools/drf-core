import urllib
import logging
import json

from rest_framework.test import APITestCase, APIClient
from django.utils.encoding import force_text
from django.contrib.auth.hashers import make_password

from accounts.factories import UserFactory
from drf_core import assertion
from drf_core.sampling import Sampling

log = logging.getLogger('test')


class BaseTestCase(APITestCase, assertion.BaseAssertion):
    """
    The base class for normal test suite.
    """

    api_client = APIClient()
    sampling = Sampling()
    resource = None

    class Meta:
        """
        Meta class
        """

        abstract = True

    def setUp(self):
        super().setUp()

        # get resource URI
        uri = self.resource().get_resource_uri()

        # if resource name is empty, the resource URI should be fixed by
        # removing the last splash character
        resource_name = self.resource().resource_name

        if resource_name is None or resource_name == '':
            uri = uri[:-1]

        self.uri = uri
        self.auth = None
        self.username = None
        self.password = None
        self.api_key = None
        self.token = None

        self.setup_session()

    def build_api_url(self, fragment=None, **params):
        uri = self.uri

        if fragment:
            uri = '{}{}'.format(self.uri, fragment)

        if params:
            query_string = urllib.parse.urlencode(params)
            delimiter = '?'

            if '?' in uri:
                delimiter = '&'

            uri = '{}{}{}'.format(uri, delimiter, query_string)

        return uri

    def make_user(
        self,
        username='user', first_name=None, last_name=None, email=None,
        password='123456', is_staff=False, is_superuser=False
    ):
        """
        Create a user for testing.
        """
        assert username
        assert password
        user = UserFactory(
            username=username,
            first_name=first_name or username,
            last_name=last_name or username,
            email=email or '{}@domain.com'.format(username),
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=make_password(password)
        )

        return user

    def setup_session(
        self,
        auth='token',
        username='user', first_name=None, last_name=None, email=None,
        password='123456', is_staff=False, is_superuser=False
    ):
        """
        Prepare session before each test case.
        """
        user = self.make_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        self.authenticated_user = user
        self.auth = auth
        self.username = username
        self.password = password
        # self.api_key = user.auth_token.key
        self.token = user.auth_token.key

        if auth == 'session':
            # Log the user in for django session.
            # For other types of authentication, the authentication
            # will need to be embedded in the API calls.
            self.api_client.client.login(
                username=self.username,
                password=self.password
            )

        return user

    def get_credentials(self):
        """ Returns the authorization header for the next api call (e.g.,
        get_json, post_json, etc).
        """
        auth = self.auth
        if not auth:
            return None

        if auth == 'apikey':
            assert self.username, 'username is required'
            assert self.api_key, 'api_key is required'

            return self.create_apikey(
                self.username,
                self.api_key
            )

        if auth == 'token':
            assert self.token, 'token is required'
            return self.create_token(self.token)

        elif auth == 'basic':
            assert self.username, 'username is required'
            assert self.password, 'password is required'

            return self.create_basic(
                username=self.username,
                password=self.password
            )

        elif auth == 'session':
            # Dothing an assume that the client has already signed in
            # in previous setup_session call
            pass

        else:
            raise 'Invalid Auth %s' % auth

    def create_apikey(self, username, api_key):
        """
        Creates & returns the HTTP ``Authorization`` header for use with
        ``ApiKeyAuthentication``.
        """
        return 'ApiKey %s:%s' % (username, api_key)

    def create_token(self, token):
        """
        Creates & returns the HTTP ``Authorization`` header for use with
        ``TokenAuthentication``.
        """
        return {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

    def create_basic(self, username, password):
        """
        Creates & returns the HTTP ``Authorization`` header for use with BASIC
        Auth.
        """
        import base64
        return 'Basic %s' % base64.b64encode(
            ':'.join([username, password]).encode('utf-8')).decode('utf-8')

    def deserialize(self, resp):
        """
        Given a ``HttpResponse`` coming back from using the ``client``, this
        method checks the ``Content-Type`` header & attempts to deserialize the
        data based on that.
        It returns a Python datastructure (typically a ``dict``) of the
        serialized data.
        """
        return json.loads(resp.content)

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    def get_json(self, fragment=None, **params):
        log.debug('---Request---')

        url = self.build_api_url(fragment, **params)

        # add credentials
        if self.auth:
            self.api_client.credentials(**self.get_credentials())

        # request to API
        self.resp = self.api_client.get(
            url,
            format='json',
        )

        try:
            self.assertValidJSONResponse(self.resp)
            self.resp_text = force_text(self.resp.content)
            self.resp_json = self.deserialize(self.resp)

            log.debug('--Response:--')
            log.debug(self.resp_json)

        except:
            pass

        return self.resp

    def get_json_ok(self, fragment=None, **params):
        """
        Expect a `get_json` return HTTP 200 OK code.
        """
        resp = self.get_json(fragment=fragment, **params)
        self.assertHttpOK(resp)
        return resp

    def get_json_bad_request(self, fragment=None, **params):
        """ An `get_json` extension that expects an HTTP 400 `bad request`
        code.
        """
        resp = self.get_json(fragment=fragment, **params)
        self.assertHttpBadRequest(resp)
        return resp

    def get_json_unauthorized(self, fragment=None, **params):
        """ A utility function for make a HTTP GET api call that doesn't
        pass authentication.
        """
        resp = self.get_json(fragment=fragment, **params)
        self.assertHttpUnauthorized(resp)

    def get_json_method_not_allowed(self, fragment=None, **params):
        """
        Makes sure that the get_list_json call returns HTTP 405 error code (
        Http Method not allowed)
        """
        resp = self.get_json(fragment=fragment, **params)
        self.assertHttpMethodNotAllowed(resp)

    def get_json_method_forbidden(self, fragment=None, **params):
        """
        Makes sure that the get_list_json call returns HTTP 403 error code (
        Http Request forbidden)
        """
        resp = self.get_json(fragment=fragment, **params)
        self.assertHttpForbidden(resp)

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------
    def post_json(self, data, fragment=None, **params):
        """ A utility function for make HTTP PUT api call. For example,

        For example:
            data = {
                'username': 'test1',
                'password': '123456',
            }
            self.post_json(data, 'login/')
        """
        log.debug('---Request---')
        url = self.build_api_url(fragment, **params)

        log.debug('POST %s' % url)
        if data:
            log.debug(data)

        # add credentials
        if self.auth:
            self.api_client.credentials(**self.get_credentials())

        # request to API
        self.resp = self.api_client.post(
            url,
            format='json',
            data=data,
        )

        try:
            # Try to decodes the response body
            # self.resp_text = force_text(self.resp.content)
            self.resp_json = self.deserialize(self.resp)
            log.debug('--Response:--')
            log.debug(self.resp_json)

        except Exception as ex:
            log.debug(ex)
            pass

        return self.resp

    def post_json_ok(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 200 `ok` code. """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpOK(resp)
        return resp

    def post_json_accepted(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 202 `accepted`
        code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpAccepted(resp)
        return resp

    def post_json_created(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 201 `created`
        code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpCreated(resp)
        if 'id' in self.resp_json:
            self.resp_object_id = int(self.resp_json['id'])

        return resp

    def post_json_unauthorized(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 201 `unauthorized`
        code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpUnauthorized(resp)
        return resp

    def post_json_bad_request(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 400 `bad request`
        code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpBadRequest(resp)
        return resp

    def post_json_application_error(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 500 `application error`
        code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpApplicationError(resp)
        return resp

    def post_json_method_not_allowed(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 405 `method not
        allowed` code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpMethodNotAllowed(resp)
        return resp

    def post_json_method_forbidden(self, data, fragment=None, **params):
        """ An `post_json` extension that expects an HTTP 403 `forbidden` code.
        """
        resp = self.post_json(data, fragment=fragment, **params)
        self.assertHttpForbidden(resp)
        return resp

    # --------------------------------------------------------------------------
    # PUT
    # --------------------------------------------------------------------------
    def put_json(self, data, fragment=None, **params):
        """ A utility function for make HTTP PUT api call. For example,

        For example:
            data = {
                'username': 'test1',
                'password': '123456',
            }
            self.put_json(data, 'login/')
        """
        log.debug('--Request:--')
        url = self.build_api_url(fragment, **params)

        log.debug('PUT %s' % url)
        if data:
            log.debug(data)

        # add credentials
        if self.auth:
            self.api_client.credentials(**self.get_credentials())

        # request to API
        self.resp = self.api_client.put(
            url,
            format='json',
            data=data,
        )

        try:
            # Try to decodes the response body
            # self.resp_text = force_text(self.resp.content)
            self.resp_json = self.deserialize(self.resp)
            log.debug('--Response:--')
            log.debug(self.resp_json)
        except:
            pass

        return self.resp

    def put_json_ok(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 200 `ok` code. """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpOK(resp)
        return resp

    def put_json_accepted(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 202 `accepted`
        code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpAccepted(resp)
        return resp

    def put_json_created(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 201 `created`
        code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpCreated(resp)
        return resp

    def put_json_unauthorized(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 401 `unauthorized`
        code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpUnauthorized(resp)
        return resp

    def put_json_bad_request(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 400 `bad request`
        code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpBadRequest(resp)
        return resp

    def put_json_application_error(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 500 `application error`
        code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpApplicationError(resp)
        return resp

    def put_json_method_not_allowed(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 405 `method not
        allowed` code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpMethodNotAllowed(resp)
        return resp

    def put_json_method_forbidden(self, data, fragment=None, **params):
        """ An `put_json` extension that expects an HTTP 403 `forbidden` code.
        """
        resp = self.put_json(data, fragment=fragment, **params)
        self.assertHttpForbidden(resp)
        return resp

    # --------------------------------------------------------------------------
    # PATCH
    # --------------------------------------------------------------------------
    def patch_json(self, data, fragment=None, **params):
        """ A utility function for make HTTP PUT api call. For example,

        For example:
            data = {
                'username': 'test1',
                'password': '123456',
            }
            self.patch_json(data, 'login/')
        """
        log.debug('--Request:--')
        url = self.build_api_url(fragment, **params)

        log.debug('PATCH %s' % url)
        if data:
            log.debug(data)

        # add credentials
        if self.auth:
            self.api_client.credentials(**self.get_credentials())

        # request to API
        self.resp = self.api_client.patch(
            url,
            format='json',
            data=data,
        )

        try:
            # Try to decodes the response body
            # self.resp_text = force_text(self.resp.content)
            self.resp_json = self.deserialize(self.resp)
            log.debug('--Response:--')
            log.debug(self.resp_json)
        except:
            pass

        return self.resp

    def patch_json_ok(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 200 `ok` code. """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpOK(resp)
        return resp

    def patch_json_accepted(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 202 `accepted`
        code.
        """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpAccepted(resp)
        return resp

    def patch_json_created(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 201 `created`
        code.
        """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpCreated(resp)
        return resp

    def patch_json_unauthorized(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 401 `unauthorized`
        code.
        """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpUnauthorized(resp)
        return resp

    def patch_json_bad_request(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 400 `bad request`
        code.
        """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpBadRequest(resp)
        return resp

    def patch_json_forbidden(self, data, fragment=None, **params):
        """ An `patch_json` extension that expects an HTTP 403 `forbidden`
        code.
        """
        resp = self.patch_json(data, fragment=fragment, **params)
        self.assertHttpForbidden(resp)
        return resp

    # --------------------------------------------------------------------------
    # DELETE
    # --------------------------------------------------------------------------
    def delete_json(self, fragment=None, **params):
        log.debug('--Request:--')
        url = self.build_api_url(fragment, **params)

        log.debug('DELETE %s' % url)

        # add credentials
        if self.auth:
            self.api_client.credentials(**self.get_credentials())

        # request to API
        self.resp = self.api_client.delete(
            url,
            format='json',
        )

        try:
            # Try to decodes the response body
            # self.resp_text = force_text(self.resp.content)
            self.resp_json = self.deserialize(self.resp)
            log.debug('--Response:--')
            log.debug(self.resp_json)
        except:
            pass

        return self.resp

    def delete_json_ok(self, fragment=None, **params):
        resp = self.delete_json(fragment=fragment, **params)
        self.assertHttpAccepted(resp)

    def delete_method_not_allowed(self, fragment=None, **params):
        resp = self.delete_json(fragment=fragment, **params)
        self.assertHttpMethodNotAllowed(resp)

    def delete_method_forbidden(self, fragment=None, **params):
        resp = self.delete_json(fragment=fragment, **params)
        self.assertHttpForbidden(resp)
