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

https://www.oauth.com/oauth2-servers/getting-ready/
