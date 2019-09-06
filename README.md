# Authlib for aiohttp


## OAuth 1.0

```python
from authlib_aiohttp import OAuth1Client


async def fetch_request_token():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    async with OAuth1Client.create() as client:
        request_token = await client.fetch_request_token(request_token_url)
```
