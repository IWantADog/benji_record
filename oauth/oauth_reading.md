# oauth

https://www.oauth.com/

## caption 1

### creating a application

The registration process typically involves creating an account on the service’s website, then entering basic information about the application such as the name, website, logo, etc. After registering the application, you’ll be given a `client_id` (and a `client_secret` in some cases) that you’ll use when your app interacts with the service.

> 在认证提供商上注册`application`，获取`client_id`和 `client_secret`。

One of the most important things when creating the application is to register one or more `redirect URLs` the application will use. The redirect URLs are where the OAuth 2.0 service will return the user to after they have authorized the application. __It is critical that these are registered, otherwise it is easy to create malicious applications that can steal user data. This is covered in more detail later in this book.__

> `redirect_url` 也需要被注册，出于安全的考虑。

### Redirect URLs and State

为了安全`redirect_url`必须为https

Most services treat redirect URL validation as an exact match. This means a redirect URL of `https://example.com/auth` would not match `https://example.com/auth?destination=account`. __It is best practice to avoid using query string parameters in your redirect URL, and have it include just a path.__

> 避免使用查询字段，直接使用路径更好。

### state how to use

todo

## chapter 2

[github docs](https://docs.github.com/en/rest)

### what it is

`authorize_url` & `api_base_url` & `token_url`

### http header 

`Authorization: Bearer e2f8c8e136c73b1e909bb1021b3b4c29`

### OAuth is a authorization protocol

OAuth was designed as an authorization protocol, so the end result of every OAuth flow is the app obtains an `access token` in order to be able to access or modify something about the user’s account. __The access token itself says nothing about who the user is.__

There are several ways different services provide a way for an app to find out the identity of the user. __A simple way is for the API to provide a “user info” endpoint which will return the authenticated user’s name and other profile info when an API call is made with an access token.__ While this is not something that is part of the OAuth standard, it’s a common approach many services have taken. __A more advanced and standardized approach is to use `OpenID Connect`, an OAuth 2.0 extension. OpenID Connect is covered in more detail in .__

> `OAuth`是一个授权的协议，通过`OAuth`应用最终会得到一个`access token`，其中不包含用户信息。

> 认证服务商额外增加一个`用户信息接口`，使应用通过发送携带`access token`(ie. `Authorization: Bearer e2f8c8e136c73b1e909bb1021b3b4c29`)的请求获取用户的信息。

> 更高级会使用 `OpenID`。它是`OAuth 2.0`的扩展。

### get user info

- 解析`ID token`
- 通过携带`ID token`的请求向认证服务商获取用户信息
- 使用`access token`从认证服务商提供的接口获取用户信息

### json web token

todo

## chapter 4 [Server-Side Apps]

### Step-by-step
The high level overview is this:

- Create a log-in link with the app’s client ID, redirect URL, and state parameters
- The user sees the authorization prompt and approves the request
- The user is redirected back to the app’s server with an auth code
- The app exchanges the auth code for an access token

## chapter 5 [Single-Page Apps]


## chapter 7 [Making Authenticated Requests]

__The thing to keep in mind is that access tokens are opaque to the client, and should only be used to make API requests and not interpreted themselves.__

If you are trying to find out whether your access token has expired, you can either store the expiration lifetime that was returned when you first got the access token, or just try to make the request anyway, and get a new access token if the current one has expired.


Keep in mind that at any point the user can revoke an application , so your application needs to be able to handle the case when refreshing the access token also fails. 


## 8 The Client ID and Secret

The client_secret is a secret known only to the application and the authorization server. It must be sufficiently random to not be guessable, which means you should avoid using common UUID libraries which often take into account the timestamp or MAC address of the server generating it. A great way to generate a secure secret is to use a cryptographically-secure library to generate a 256-bit value and converting it to a hexadecimal representation.

> 关于`client_secret`

## 9 Authorization

如何实现 oauth2 认证服务

### request parameter
- response_type
- client_id
- redirect_uri
- scope
- state

### 9.2 Requiring User Login

Typically sites like Twitter or Facebook expect their users are signed in most of the time, so they provide a way for their authorization screens to give the user a streamlined experience by not requiring them to log in each time. However, based on the security requirements of your service as well as the third-party applications, it may be desirable to require or give developers the option to require the user to log in each time they visit the authorization screen.

> 对于认证服务，需要决定是否每次通过第三方登录，都需要让用户重新登录。

In any case, if the user is signed out, or doesn’t yet have an account on your service, you’ll need to provide a way for them to sign in or create an account on this screen.

> 对于登出用户和没有账户的用户，还需要在授权界面提供重新登录和注册的接口

In enterprise environments, a common technique is to use `SAML`, an XML-based standard for authentication, to leverage the existing authentication mechanism at the organization, while avoiding creating another username/password database.

> SAML

### 9.3 The Authorization Interface

#### The requested or effective lifetime

Most services do not automatically expire authorizations, and instead expect the user to periodically review and revoke access to apps they no longer want to use. However some services provide limited token lifetime by default, and either allow the application to request a longer duration, or force users to re-authorize the app after the authorization is expired.

> 很多服务不主动使认证过期，除非用户主动删除。不过许多服务会为认证增加时间限制，允许用户请求一个更长的持续时间，或是强制用户重新授权app当授权过期。


### 9.4 The Authorization Response

Depending on the grant type, the authorization server will respond with either an `authorization code` or an `access token`.

#### Generating the Authorization Code

__The authorization code must expire shortly after it is issued.__ The OAuth 2.0 spec recommends a maximum lifetime of 10 minutes, but in practice, most services set the expiration much shorter, around 30-60 seconds. The authorization code itself can be of any length, but the length of the codes should be documented.

> authorization code的有效期一般较短。

Because authorization codes are meant to be short-lived and single-use, they are a great candidate to implement as self encoded. With this technique, you can avoid storing authorization codes in a database, and instead, encode all of the necessary information into the code itself. You can use either a built-in encryption library of your server-side environment, or a standard such as JSON Web Signature (JWS). Since this string only needs to be understandable to your authorization server, there is no requirement to implement this using a standard such as JWT. That said, if you don’t have an already-available encryption library easily accessible, a JWT is a great candidate since there are libraries available in many languages.

> 由于authorization code的有效期较短，所以将它存在数据库中不是一个好的选择。通过对数据进行编码更为合理。


The information that will need to be associated with the authorization code is the following.

- `client_id` – The client ID (or other client identifier) that requested this code
- `redirect_uri` – The redirect URL that was used. This needs to be stored since the access token request must contain the same redirect URL for verification when issuing the access token.
- `User info` – Some way to identify the user that this authorization code is for, such as a user ID.
- `Expiration Date` – The code needs to include an expiration date so that it only lasts a short time.
- `Unique ID` – The code needs its own unique ID of some sort in order to be able to check if the code has been used before. A database ID or a random string is sufficient.

> authorization code的构成。

Once you’ve generated the authorization code。 The parameters to be added to the query string of the redirect URL are as follows:


- code: This parameter contains the authorization code which the client will later exchange for an access token.

- state: If the initial request contained a state parameter, the response must also include the exact value from the request. The client will be using this to associate this response with the initial request.

> state的功能是什么

### 9.5 Security Considerations

Phishing Attacks

Clickjacking

Redirect URL Manipulation

## 10 Scope

通过scope授权第三方应用获取用户部分信息。

### 10.1 Defining Scopes

A good place to start with defining scopes is to define read vs write separately.

> 把只读的和可修改的scope分开是一个好的实践。

## 11 Redirect URIs

重定向url很重要。oauth提供商只能从重定向用户到已注册的url。

If a client wishes to include request-specific data in the redirect URL, it can instead use the “state” parameter to store data that will be included after the user is redirected. It can either encode the data in the state parameter itself, or use the state parameter as a session ID to store the state on the server.

> 如果重定向请求中需要包含额外的信息，可以将额外的信息直接存放在`state`中或将`state`设置为一个ID，application可以通过state从数据库中获取信息。

### 11.3 Redirect URL Validation

- 注册application时检测redirect url是否合法
- 获取authorization code时，验证redirect url是否存在与application中
- 获取access_token是，验证redirect url是否存在与application中

## 12 Access Token

### 12.1 Authorization Code Request

#### Request Parameters

- grant_type

    The grant_type parameter must be set to “authorization_code”.

- code
- redirect_uri
- client_id

#### Verifying the authorization code grant

After checking for all required parameters, and authenticating the client if the client was issued a secret, the authorization server can continue verifying the other parts of the request.

The server then checks if the authorization code is valid, and has not expired. The service must then verify that the authorization code provided in the request was issued to the client identified. Lastly, the service must ensure the redirect URI parameter present matches the redirect URI that was used to request the authorization code.

> 验证authorization code。

#### Security Considerations

Preventing replay attacks

> 所有的authorization code只能使用一次。对于重复使用的authorization code可以视为系统攻击，可以将之前的access_token取消。

### 12.3 Client Credentials

The Client Credentials grant is used when applications request an access token to access their own resources, not on behalf of a user.

> 获取注册application的相关信息。

#### Request Parameters

- grant_type

    The grant_type parameter must be set to client_credentials.

- scope
- Client Authentication

    The client needs to authenticate themselves for this request. Typically the service will allow either additional request parameters client_id and client_secret, or accept the client ID and secret in the HTTP Basic auth header.

### 12.4 Access Token Response

The response with an access token should contain the following properties:

- `access_token` (required) The access token string as issued by the authorization server.

- `token_type` (required) The type of token this is, typically just the string “bearer”.

- `expires_in` (recommended) If the access token expires, the server should reply with the duration of time the access token is granted for.

    > access_token的有效时间。

- `refresh_token` (optional) If the access token will expire, then it is useful to return a refresh token which applications can use to obtain another access token. However, tokens issued with the implicit grant cannot be issued a refresh token.

    > 当access_token过期后，application通过refresh_token换取新的token。

- `scope` (optional) If the scope the user granted is identical to the scope the app requested, this parameter is optional. If the granted scope is different from the requested scope, such as if the user modified the scope, then this parameter is required.

    > 如果认证服务授权的范围和application请求的范围相同，该字段可以省略。如果不相同，该字段是必须的。

When responding with an access token, the server must also include the additional Cache-Control: no-store and Pragma: no-cache HTTP headers to ensure clients do not cache this request.

> 当请求返回后，认证服务提供商需要在响应的http header中增加`Cache-Control: no-store` & `Pragma: no-cache`保证客户端不会缓存请求。

### 12.5 Self-Encoded Access Tokens

Self-encoded tokens provide a way to avoid storing tokens in a database by encoding all of the necessary information in the token string itself. The main benefit of this is that API servers are able to verify access tokens without doing a database lookup on every API request, making the API much more easily scalable.

> 自编码access_token可以避免将access_token存储在数据库中。


json web token (JWT)

Note: Anyone can read the token information by base64-decoding the middle section of the token string. For this reason, it’s important that you do not store private information or information you do not want a user or developer to see in the token. If you want to hide the token information, you can use the JSON Web Encryption spec to encrypt the data in the token.

> 由于access_token可以使用`base64-decoding`编码。所以使用access_token时不应该存储敏感信息。如果想要加密信息，可以使用`JSON Web Encryption`。

#### Invalidating

Because the token can be verified without doing a database lookup, there is no way to invalidate a token until it expires. You’ll need to take additional steps to invalidate tokens that are self-encoded. See Refreshing Access Tokens for more information.

> 对于自编码的access_token的过期验证，需要额外的验证步骤。

### 12.6 Access Token lifetime

#### Short-lived access tokens and long-lived refresh tokens

A common method of granting tokens is to use a combination of access tokens and refresh tokens for maximum security and flexibility. The OAuth 2.0 spec recommends this option, and several of the larger implementations have gone with this approach.

通常的做法是使用 access_token 和 refresh_token 的混合。

传统的做法是服务提供商返回 access_token 时，同时返回 refresh_token 。 access_token有有效期，但refresh_token长期有效。当 access_token 过期时，applicaiton通过refresh_token换取新的access_token。

对于自编码的access_token由于服务商无法主动过期。所以自编码的access_token只有很短的有效期，迫使applicaiton不但地更新。这也使服务商有机会主动过期一个access_token。

#### Short-lived access tokens and no refresh tokens

If you want to ensure users are aware of applications that are accessing their account, the service can issue relatively short-lived access tokens without refresh tokens. The access tokens may last anywhere from the current application session to a couple weeks. When the access token expires, the application will be forced to make the user sign in again, so that you as the service know the user is continually involved in re-authorizing the application.

> 对于比较敏感或是风险较高的信息。服务提供商可以提供短期的access_token并且不提供refresh token。这会导致当access_token过期时，applicaiton必须强迫用户重新登录。

#### Non-expiring access tokens

> 对于自编码的access token，服务商无法使其过期。对于这种情况，需要将数据存储到数据库中。

### 12.7 Refreshing Access Tokens

#### Request Parameters

- grant_type (required)

    The grant_type parameter must be set to “refresh_token”.

- refresh_token (required)
- scope (optional)
    > scope只能与起始请求的scope相同。默认可以省略。

> 刷新access token之后，可以返回新的refresh token。如果不返回，则默认继续使用旧的。

### 13 Listing Authorizations

用户授权自己账户给许多的applicaiton，认证提供商需要提供一个列表包含所有用户授权的application。

### 13.1 Revoking Access

#### Token Database

对于存在数据库中的`access token`，只需删除相关用户的数据即可。

#### Self-Encoded Tokens

对于自编码的`access token`，提供商没办法主动使`access token`过期。
1. 等待`access token`过期。
2. 使`refresh token`过期使applicaton无法获取新的`access token`。
3. 不允许applicaiton获取新的`access token`。

> 这也是将自编码`access token`的有效时间应该较短的主要原因。

## 15 OAuth for Native Apps

对于`native app`不同于`browser-based app`，前者获取一个`secret-id`后，需要写入application中。这也提供了通过反编译获取`secret-id`的可能。所以对于`native app`需要一种不需要`secret-id`的oauth的认证流程。



<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes
