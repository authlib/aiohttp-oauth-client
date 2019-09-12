from aiohttp import ClientSession
from authlib.oauth2.client import OAuth2Client as _OAuth2Client
from .base import ClientMixin, OAuth2Request


class OAuth2Client(ClientMixin, _OAuth2Client):
    """The OAuth 2.0 Client for ``aiohttp.ClientSession``. Here
    is how it works::

        async with OAuth2Client.create(client_id, client_secret, ...) as client:
            await client.fetch_token(...)
    """
    SESSION_REQUEST_PARAMS = (
        'timeout', 'allow_redirects', 'max_redirects',
        'expect100', 'read_until_eof',
        'json', 'cookies', 'skip_auto_headers', 'compress',
        'chunked', 'raise_for_status', 'proxy', 'proxy_auth',
        'verify_ssl', 'fingerprint', 'ssl_context', 'ssl',
        'proxy_headers', 'trace_request_ctx',
    )


    def __init__(self, client_id=None, client_secret=None,
                 token_endpoint=None, token_endpoint_auth_method=None,
                 scope=None, redirect_uri=None,
                 token=None, token_placement='header', token_updater=None, **kwargs):
        session = ClientSession(request_class=OAuth2Request)
        _OAuth2Client.__init__(
            self, session=session,
            client_id=client_id, client_secret=client_secret,
            client_auth_method=token_endpoint_auth_method,
            refresh_token_url=token_endpoint,
            scope=scope, redirect_uri=redirect_uri,
            token=token, token_placement=token_placement,
            token_updater=token_updater, **kwargs
        )

    async def _fetch_token(self, url, body='', headers=None, auth=None,
                           method='POST', **kwargs):
        if method.upper() == 'POST':
            async with self.session.post(
                    url, data=dict(url_decode(body)), headers=headers,
                    auth=auth, **kwargs) as resp:
                token = await self._parse_token(resp, 'access_token_response')
                return self.parse_response_token(token)
        else:
            async with self.session.get(
                    url, params=dict(url_decode(body)), headers=headers,
                    auth=auth, **kwargs) as resp:
                token = await self._parse_token(resp, 'access_token_response')
                return self.parse_response_token(token)

    async def _refresh_token(self, url, refresh_token=None, body='', headers=None,
                             auth=None, **kwargs):
        async with self.session.post(
                url, data=dict(url_decode(body)), headers=headers,
                auth=auth, **kwargs) as resp:
            token = await self._parse_token(resp, 'refresh_token_response')
            if 'refresh_token' not in token:
                self.token['refresh_token'] = refresh_token

            if callable(self.token_updater):
                await self.token_updater(self.token)

            return self.token

    async def _parse_token(self, resp, hook_type):
        for hook in self.compliance_hook[hook_type]:
            resp = await hook(resp)
        token = await resp.json()
        return token

    async def _request(self, method, url, **kwargs):
        if self.refresh_token_url and self.token.is_expired():
            refresh_token = self.token.get('refresh_token')
            if refresh_token:
                await self.refresh_token(refresh_token=refresh_token)
        return await self.session.request(
            method, url, auth=self.token_auth, **kwargs)
