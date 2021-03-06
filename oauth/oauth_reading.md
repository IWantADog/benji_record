# oauth

https://www.oauth.com/

## creating a application

在认证提供商上注册`application`，需要提供`name` `website` `logo` `redirect URLs`。注册完成之后会得到`client_id`和 `client_secret`。

- client_id: 每个applicaiton的唯一标记。
- client_secret: 可以理解为每个applicaiton的密码。

为了安全`redirect_url`必须为https。

许多服务对待`redirect url`会使用准确校验，这意味着redirect url中不应该包含查询参数，而只应该包含url路径。例如`https://example.com/auth` 不会匹配 `https://example.com/auth?destination=account`。

## Base

`OAuth`是一个授权的协议，它的实质是获取用户的授权并代替用户从服务提供商获取数据。

通过`OAuth` application 最终会得到一个`access token`，其中不包含用户信息，但application可以通过这个`access token`从服务提供商获取用户的资源数据。

如果`application`想要通过 oauth2.0 获取用户的信息。认证服务提供商需要额外增加一个`用户信息接口`，使应用可以通过`access token`的获取用户的信息。

oauth服务提供商会提供两个`endpoint`:

- `authorization endpoint`: 启动认证流程，用户选择是否同意授权，最终返回`authorization code`
- `access token endpoint`: 通过`authorization code`交换`access token`

更高级服务提供商会使用 `OpenID`。它是`OAuth 2.0`的扩展，用来获取用户的详细信息。[goto OpenID](#OpenID_Connect)

### 通过oauth2.0获取用户数据的方式

- 解析`ID token`（JWT格式）
- 通过携带`ID token`的请求向认证服务商获取用户信息
- 使用`access token`从认证服务商提供的接口获取用户信息


## Server-Side Apps

### Authorization Code Grant

[code and access token request and response paramenter](https://www.oauth.com/oauth2-servers/server-side-apps/authorization-code/)

### Step-by-step

`server side app`大概的整个认证流程。

The high level overview is this:

- Create a log-in link with the app’s client ID, redirect URL, and state parameters
- The user sees the authorization prompt and approves the request
- The user is redirected back to the app’s server with an auth code
- The app exchanges the auth code for an access token

## Single-Page Apps

对于`single-page apps`，由于它的源码在浏览器中可见，所以使用`secret_id`不安全。`single-page app`获取`authorization code`的过程与`server-side app`相同，唯一不同点在`single-page app`获取`access token`时请求中不需要携带`secret id`。

对于不需要发送`secret id`的应用。保证安全的方式一般是通过`state`和`redirect url`。


## Making Authenticated Requests

需要牢记的一点，`access token`对于`application`是不透明的，`applicatoin`不应该想着去`decode` `access token`，即使`access token`是按照`JWT`编码的。__`access token`只应该被用于请求API__。因为`access token`的格式可能会修改。


## Authorization

如何实现 oauth2 认证服务

### request parameter
- response_type: code
- client_id
- redirect_uri
- scope
- state

### Requiring User Login

Typically sites like Twitter or Facebook expect their users are signed in most of the time, so they provide a way for their authorization screens to give the user a streamlined experience by not requiring them to log in each time. However, based on the security requirements of your service as well as the third-party applications, it may be desirable to require or give developers the option to require the user to log in each time they visit the authorization screen.

> 对于认证服务，需要决定用户每次访问授权流程，是否都需要重新登录。

In any case, if the user is signed out, or doesn’t yet have an account on your service, you’ll need to provide a way for them to sign in or create an account on this screen.

> 对于登出用户和没有账户的用户，还需要在授权界面提供重新登录和注册的接口

In enterprise environments, a common technique is to use `SAML`, an XML-based standard for authentication, to leverage the existing authentication mechanism at the organization, while avoiding creating another username/password database.

> SAML

### The Authorization Interface

The requested or effective lifetime

Most services do not automatically expire authorizations, and instead expect the user to periodically review and revoke access to apps they no longer want to use. However some services provide limited token lifetime by default, and either allow the application to request a longer duration, or force users to re-authorize the app after the authorization is expired.

> 很多服务不主动使认证过期，除非用户主动删除。不过许多服务会为认证增加时间限制，允许用户请求一个更长的持续时间，或是强制用户重新授权app当授权过期。


### The Authorization Response

#### Generating the Authorization Code

__The authorization code must expire shortly after it is issued.__ The OAuth 2.0 spec recommends a maximum lifetime of 10 minutes, but in practice, most services set the expiration much shorter, around 30-60 seconds. The authorization code itself can be of any length, but the length of the codes should be documented.

> authorization code的有效期一般较短。

Because `authorization codes` are meant to be short-lived and single-use, they are a great candidate to implement as self encoded. With this technique, you can avoid storing authorization codes in a database, and instead, encode all of the necessary information into the code itself. You can use either a built-in encryption library of your server-side environment, or a standard such as JSON Web Signature (JWS). Since this string only needs to be understandable to your authorization server, there is no requirement to implement this using a standard such as JWT. __That said, if you don’t have an already-available encryption library easily accessible, a JWT is a great candidate since there are libraries available in many languages.__

> 由于authorization code的有效期较短，所以将它存在数据库中不是一个好的选择。通过对数据进行编码更为合理(使用`JWT`是一个较好的选择)。


`authorization code`的构成。

- `client_id` – The client ID (or other client identifier) that requested this code
- `redirect_uri` – The redirect URL that was used. This needs to be stored since the access token request must contain the same redirect URL for verification when issuing the access token.
- `User info` – Some way to identify the user that this authorization code is for, such as a user ID.
- `Expiration Date` – The code needs to include an expiration date so that it only lasts a short time.
- `Unique ID` – The code needs its own unique ID of some sort in order to be able to check if the code has been used before. A database ID or a random string is sufficient.

`authorization flow`的返回值:

- code: `authorization code`

- state: application传过来的数据

    - state在用户完成授权被重定向到`redirect url`时，applicaiton在授权流程开始时设置的state对应的数据，会被完整的返回给application。这提供了一个在可以维持数据的机会。
    - state可以用来防止`CSRF`。

### Security Considerations

Phishing Attacks

Clickjacking

Redirect URL Manipulation

## Scope

通过scope限制`applicaiton`获取用户信息。

把只读的和可修改的scope分开是一个好的实践。

## Redirect URIs

重定向url很重要。oauth提供商只能重定向用户到已注册的url。

> 如果重定向请求中需要包含额外的信息，可以将额外的信息直接存放在`state`中或将`state`设置为一个ID，application可以通过state从数据库中获取信息。

### Redirect URL Validation

- 注册application时检测redirect url是否合法
- 获取authorization_code时，验证redirect_url是否存在与application中
- 获取access_token是，验证redirect_url是否存在与application中

## Access Token 

`access token`必须是加密过的；使用`access token`必须使用https。

### Authorization Code Request

获取access_token的请求参数组成：

- grant_type: 必须为`authorization_code`
- code: authorization code
- redirect_uri
- client_id

#### Security Considerations

所有的authorization code只能使用一次。对于重复使用的authorization code可以视为系统攻击，可以将之前的access_token取消。

对于存储在数据库中的`code`，只需要在被使用一次之后将其标记为 __已使用__ 即可。

对于自编码的`code`，可以将`code`存储在缓存中并设置过期时间。

### Password Grant

请求参数:

- grant_type (required) – 必须为`password`.
- username (required) – The user’s username.
- password (required) – The user’s password.
- scope (optional) – The scope requested by the application.
- Client Authentication (required if the client was issued a secret)

### Client Credentials

application获取`access token`以获取本身注册的相关信息。

请求参数:

- grant_type: 必须为`client_credentials`
- scope
- Client Authentication

    > The client needs to authenticate themselves for this request. Typically the service will allow either additional request parameters client_id and client_secret, or accept the client ID and secret in the HTTP Basic auth header.

### Access Token Response

`access token`响应的参数构成:

- `access_token` (required) The access token string as issued by the authorization server.
- `token_type` (required) The type of token this is, typically just the string __bearer__.

- `expires_in` (recommended) If the access token expires, the server should reply with the duration of time the access token is granted for.

    > access_token的有效时间。

- `refresh_token` (optional) If the access token will expire, then it is useful to return a refresh token which applications can use to obtain another access token. However, tokens issued with the implicit grant cannot be issued a refresh token.

    > 当access_token过期后，application通过refresh_token换取新的token。

- `scope` (optional) If the scope the user granted is identical to the scope the app requested, this parameter is optional. If the granted scope is different from the requested scope, such as if the user modified the scope, then this parameter is required.

    > 如果认证服务授权的范围和application请求的范围相同，该字段可以省略。如果不相同，该字段是必须的。

当请求返回后，认证服务提供商需要在响应的http header中增加`Cache-Control: no-store` & `Pragma: no-cache`保证客户端不会缓存请求。

### Self-Encoded Access Tokens

Self-encoded tokens provide a way to avoid storing tokens in a database by encoding all of the necessary information in the token string itself. The main benefit of this is that API servers are able to verify access tokens without doing a database lookup on every API request, making the API much more easily scalable.

> 自编码access_token可以避免将access_token存储在数据库中。通过`access_token`不需要使用数据库搜索，可以方便地扩展服务。

json web token (JWT)

由于access_token可以使用`base64-decoding`编码。所以使用access_token时不应该存储敏感信息。如果想要加密信息，可以使用`JSON Web Encryption`。

#### Invalidating

对于自编码的access_token服务端无法主动无效，可以通过设置过期时间来处理。

### Access Token lifetime

#### Short-lived access tokens and long-lived refresh tokens

A common method of granting tokens is to use a combination of access tokens and refresh tokens for maximum security and flexibility. The OAuth 2.0 spec recommends this option, and several of the larger implementations have gone with this approach.

通常的做法是使用 access_token 和 refresh_token 的混合。

传统的做法是服务提供商返回 access_token 时，同时返回 refresh_token 。 access_token有有限期限，但refresh_token永不过期。当 access_token 过期时，applicaiton通过refresh_token换取新的access_token。

对于自编码的access_token由于服务商无法主动过期。所以自编码的access_token只有很短的有效期，迫使applicaiton不但地更新。这也使服务商有机会主动过期一个access_token。

#### Short-lived access tokens and no refresh tokens

对于比较敏感或是风险较高的信息。服务提供商可以提供短期的access_token并且不提供refresh token。这会导致当access_token过期时，applicaiton必须强迫用户重新登录。

#### Non-expiring access tokens

对于自编码的access token，服务商将无法删除token。

对于这种情况，只能将`access token`存储到数据库中。

### Refreshing Access Tokens

请求参数:

- grant_type (required): 必须为 __refresh_token__。
- refresh_token (required)
- scope (optional): scope只能与起始请求的scope相同。默认可以省略。

> 刷新access token之后，可以返回新的refresh token。如果不返回，则默认继续使用旧的。

## Listing Authorizations

用户授权自己账户给许多applicaiton，认证提供商需要提供一个列表包含所有用户授权的application。

### Revoking Access

删除发布的`access token`

`Token Database`: 

对于存在数据库中的`access token`，只需删除相关用户的数据即可。

`Self-Encoded Tokens`:

对于自编码的`access token`，提供商没办法主动使`access token`过期。

1. 等待`access token`过期。
2. 使`refresh token`过期使applicaton无法获取新的`access token`。
3. 不允许applicaiton获取新的`access token`。

> 这也是将自编码`access token`的有效时间应该较短的主要原因。

## OAuth for Native Apps

对于`native app`不同于`browser-based app`，前者获取一个`secret-id`后，需要写入application中。这也提供了通过反编译获取`secret-id`的可能。所以对于`native app`需要一种不需要`secret-id`的oauth的认证流程。

## Terminology Reference

OAuth defines four roles:

- Resource owner (the user)
- Resource server (the API)
- Authorization server (can be the same server as the API)
- Client (the third-party app)

## Differences Between OAuth 1 and 2

oauth2 是 oauth1 的重写。oauth2 不向后兼容 oauth1。应该将oauth1与oauth2视为两个完全不同的协议。

### User Experience and Alternative Token Issuance Options

oauth1开始时有3种`flow`，后来随着发展逐渐合为一个`flow`。但是这个唯一的`flow`对`web-base applicaiton`支持的很好，对于其他的的applicaiton支持不理想。

oauth2意识到问题，所以重新支持了多种`flow`，并且将其命名为`grant type`。oauth2支持多种applicaiton类型，并且支持自定义扩展。

oauth2支持的认证类型:

- Authorization Code: 支持`web-base applicaiton` 和 `native applicaiton`。
- Password: oauth2协议中支持通过`username & password`认证。不过这种方式，只应该被可信任的`client`使用，比如服务提供商自己内部的`client`。不能暴露给第三方app使用，因为这有可能暴露用户的`username & password`给第三方app。
- Client Credentials: application可以通过这种方式，用`access token`交换`client_id` & `client_secret`。
- Device Flow: oauth2的扩展认证方式，适用于没有`web browser`的设备。

### Performance at Scale

oauth1不利于扩展。

## OpenID_Connect

oauth2 是一个委托协议，第三方app通过`access token`获取用户的授权，但它不需要知道用户的身份。

`OpenID` 在 `oauth2` 的上层增加了用户身份层，用来提供用户的信息，也允许客户端建立一个登录session。

### Authorization vs Authentication

说明`access token`特性，贴切的例子：

> When you check in to a hotel, you get a key card which you can use to enter your assigned room. You can think of the key card as an access token. The key card says nothing about who you are, or how you were authenticated at the front desk, but you can use the card to access your hotel room for the duration of your stay. Similarly, an OAuth 2.0 access token doesn’t indicate who a user is, it just is the thing you can use to access data, and it may expire at some point in the future.

### ID Tokens

application可以向服务提供商发送`OpenID Connect Request`并带上`access token`，获取`ID token`。

`ID token`不同与`access token`，`access token`applicaiton可能无法理解，`ID token`是applicaiton可以解析并理解的。

`ID token`一般使用`JWT(Json Web Token)`对数据进行编码。

通过 `OpenID` application可以获得用户受保护的信息。

## IndieAuth

[IndieAuth](https://indieauth.net/)

`IndieAuth`是一个基于`oauth2`的去中心化的身份协议，通过`url`识别用户和applicaiton。

所有的用户ID都是url，所有application通过它们的url进行区分。

IndieAuth builds upon the OAuth 2.0 framework as follows:

- Specifies a mechanism and format for identifying users (a resolvable URL)
- Specifies a method of discoverinig the authorization and token endpoints given a profile URL
- Specifies a format for the Client ID (also as resolvable URL)
- All clients are public clients, as client secrets are not used
- Client registration is not necessary, since all clients must use a resolvable URL as their Client ID
- Redirect URI registration is accomplished by the application publicizing their valid redirect URLs on their website
- Specifies a mechanism for a token endpoint and authorization endpoint to communicate, similiar to token introspection but for authorization codes

### Discovery

以`IndieAuth`方式认证的用户，认证时需要输入认证服务商提供给用户的url。applicaiton通过用户的url获取后续认证需要的信息。

[detail about IndieAuth](https://www.w3.org/TR/indieauth/#discovery-by-clients)

### IndieAuth Sign-In Workflow

[IndieAuth Sing-In Workflow](https://www.w3.org/TR/indieauth/#authorization-code-verification)

## Map of OAuth 2.0 Specs

[Map of OAuth2.0 Specs](https://www.oauth.com/oauth2-servers/map-oauth-2-0-specs/)

## Tools and Libraries

[Tools and Libraries](https://www.oauth.com/oauth2-servers/tools-and-libraries/)