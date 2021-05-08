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


https://www.oauth.com/oauth2-servers/server-side-apps/









