# aiohttp OAuth Clients


## OAuth 1.0 Client

Taking Twitter as an example on how to use `OAuth1Client`.

```python
from aiohttp_oauth_client import OAuth1Client
```

### 1. Fetch Temporary Credential

For OAuth 1.0, the first step is requesting a temporary credential (aka
request token).


```python
client_id = '__YOUR_TWITTER_CLIENT_ID__'
client_secret = '__YOUR_TWITTER_CLIENT_SECRET__'

async def fetch_request_token():
    url = 'https://api.twitter.com/oauth/request_token'

    async with OAuth1Client(client_id, client_secret) as session:
        request_token = await session.fetch_request_token(url)
        return request_token
```

This `fetch_request_token` method will return the temporary credential like:

```
{'oauth_token': 'Ih....Jw', 'oauth_token_secret': 'gr...GE', 'oauth_callback_confirmed': 'true'}
```

We can test this function with:

```py
# twitter.py

import asyncio
from aiohttp_oauth_client import OAuth1Client

client_id = '__YOUR_TWITTER_CLIENT_ID__'
client_secret = '__YOUR_TWITTER_CLIENT_SECRET__'

async def fetch_request_token():
    url = 'https://api.twitter.com/oauth/request_token'

    async with OAuth1Client(client_id, client_secret) as session:
        request_token = await session.fetch_request_token(url)
        return request_token


async def main():
    request_token = await fetch_request_token()
    print(request_token)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```


### 2. Redirect to Authorization Endpoint

The second step is to generate the authorization URL:

```py
def create_authorization_url(request_token):
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'
    client = OAuth1Client(client_id, client_secret)
    url = client.create_authorization_url(authenticate_url, request_token['oauth_token'])
    return url
```

This step is synchronized, no need for `async` and `await`. Passing the
`request_token` we got from the first step, we would get a url like:

```
https://api.twitter.com/oauth/authenticate?oauth_token=Ih....Jw
```

Then visit this URL with your browser, and approve the request. Twitter
will redirect back to your default `redirect_uri` you registered in Twitter.

If you want to redirect to your specified URL, rewrite the code like:

```py
def create_authorization_url(request_token):
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'
    client = OAuth1Client(client_id, client_secret, redirect_uri='https://your-defined-url')
    url = client.create_authorization_url(authenticate_url, request_token['oauth_token'])
    return url
```

### 3. Fetch Access Token

The last step is to fetch the access token. In previous step, twitter
will redirect back to a URL, for instance, something like:

```
https://your-domain.org/auth?oauth_token=Ih...Jw&oauth_verifier=fcg..1Dq
```

We will use the `oauth_verifier` in this URL to fetch access token. Here
is our code:


```py
async def fetch_access_token(request_token, oauth_verifier):
    url = 'https://api.twitter.com/oauth/access_token'
    async with OAuth1Client(client_id, client_secret) as session:
        session.token = request_token
        token = await session.fetch_access_token(url, oauth_verifier)
        return token


# if you specified redirect_uri in previous step, create the session with
# OAuth1Client(client_id, client_secret, redirect_uri='....')
```

We can test this function with:

```py
# twitter.py

import asyncio
from aiohttp_oauth_client import OAuth1Client

client_id = '__YOUR_TWITTER_CLIENT_ID__'
client_secret = '__YOUR_TWITTER_CLIENT_SECRET__'

async def fetch_access_token(request_token, oauth_verifier):
    url = 'https://api.twitter.com/oauth/access_token'
    async with OAuth1Client(client_id, client_secret) as session:
        session.token = request_token
        token = await session.fetch_access_token(url, oauth_verifier)
        return token

async def main():
    # from step 1
    request_token = {
        'oauth_token': 'Ih....Jw',
        'oauth_token_secret': 'gr...GE',
        'oauth_callback_confirmed': 'true'
    }
    # from step 2
    verifier = 'fcg..1Dq'
    token = await fetch_access_token(request_token, verifier)
    print(request_token)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```


## OAuth 2.0 Client

```python
from aiohttp_oauth_client import OAuth2Client

```


## OAuth 2.0 Assertion

```python
from aiohttp_oauth_client import AssertionClient
```
