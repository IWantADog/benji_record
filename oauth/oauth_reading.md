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

Because authorization codes are meant to be short-lived and single-use, they are a great candidate to implement as self encoded. With this technique, you can avoid storing authorization codes in a database, and instead, encode all of the necessary information into the code itself. You can use either a built-in encryption library of your server-side environment, or a standard such as JSON Web Signature (JWS). Since this string only needs to be understandable to your authorization server, there is no requirement to implement this using a standard such as JWT. That said, if you don’t have an already-available encryption library easily accessible, a JWT is a great candidate since there are libraries available in many languages.


The information that will need to be associated with the authorization code is the following.

> authorization code 的构成

- `client_id` – The client ID (or other client identifier) that requested this code
- `redirect_uri` – The redirect URL that was used. This needs to be stored since the access token request must contain the same redirect URL for verification when issuing the access token.
- `User info` – Some way to identify the user that this authorization code is for, such as a user ID.
- `Expiration Date` – The code needs to include an expiration date so that it only lasts a short time.
- `Unique ID` – The code needs its own unique ID of some sort in order to be able to check if the code has been used before. A database ID or a random string is sufficient.