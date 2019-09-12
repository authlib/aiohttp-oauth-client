from aiohttp import ClientSession
from authlib.oauth2.rfc7521 import AssertionClient as _AssertionClient
from authlib.oauth2.rfc7523 import JWTBearerGrant
from .base import ClientMixin, OAuth2Request


class AssertionClient(ClientMixin, _AssertionClient):
    """The OAuth 2.0 Assertion Client for ``aiohttp.ClientSession``. Here
    is how it works::

        async with AssertionClient(token_url, issuer, ...) as client:
            await client.get(...)
    """
    JWT_BEARER_GRANT_TYPE = JWTBearerGrant.GRANT_TYPE
    ASSERTION_METHODS = {
        JWT_BEARER_GRANT_TYPE: JWTBearerGrant.sign,
    }
    DEFAULT_GRANT_TYPE = JWT_BEARER_GRANT_TYPE

    def __init__(self, token_url, issuer, subject, audience, grant_type=None,
                 claims=None, token_placement='header', scope=None, **kwargs):

        session = ClientSession(request_class=OAuth2Request)
        _AssertionClient.__init__(
            self, session=session,
            token_url=token_url, issuer=issuer, subject=subject,
            audience=audience, grant_type=grant_type, claims=claims,
            token_placement=token_placement, scope=scope, **kwargs
        )

    async def _refresh_token(self, data):
        async with self.session.post(self.token_url, data=data) as resp:
            self.token = await resp.json()
            return self.token

    async def _request(self, method, url, **kwargs):
        if not self.token or self.token.is_expired():
            await self.refresh_token()
        return await self.session.request(
            method, url, auth=self.token_auth, **kwargs)
