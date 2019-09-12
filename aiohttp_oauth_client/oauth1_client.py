from yarl import URL
from aiohttp import ClientRequest, ClientSession
from authlib.oauth1 import (
    SIGNATURE_HMAC_SHA1,
    SIGNATURE_TYPE_HEADER,
)
from authlib.oauth1.client import OAuth1Client as _OAuth1Client
from .base import ClientMixin


class OAuth1Request(ClientRequest):
    def __init__(self, *args, **kwargs):
        auth = kwargs.pop('auth', None)
        data = kwargs.get('data')
        super(OAuth1Request, self).__init__(*args, **kwargs)
        self.update_oauth_auth(auth, data)

    def update_oauth_auth(self, auth, data):
        if auth is None:
            return

        url, headers, body = auth.prepare(
            self.method, str(self.url), self.headers, data)
        self.url = URL(url)
        self.update_headers(headers)
        if body:
            self.update_body_from_data(body)


class OAuth1Client(ClientMixin, _OAuth1Client):
    """The OAuth 1.0 Client for ``aiohttp.ClientSession``. Here
    is how it works::

        async with OAuth1Client(client_id, client_secret, ...) as client:
            await client.fetch_access_token(...)
    """

    def __init__(self, client_id, client_secret=None,
             token=None, token_secret=None,
             redirect_uri=None, rsa_key=None, verifier=None,
             signature_method=SIGNATURE_HMAC_SHA1,
             signature_type=SIGNATURE_TYPE_HEADER,
             force_include_body=False, **kwargs):
        session = ClientSession(request_class=OAuth1Request)
        _OAuth1Client.__init__(
            self, session=session,
            client_id=client_id, client_secret=client_secret,
            token=token, token_secret=token_secret,
            redirect_uri=redirect_uri, rsa_key=rsa_key, verifier=verifier,
            signature_method=signature_method, signature_type=signature_type,
            force_include_body=force_include_body, **kwargs)

    async def _fetch_token(self, url, **kwargs):
        async with self.post(url, **kwargs) as resp:
            text = await resp.text()
            token = self.parse_response_token(resp.status, text)
            self.token = token
            return token

    def _request(self, method, url, **kwargs):
        return self.session.request(method, url, auth=self.auth, **kwargs)
