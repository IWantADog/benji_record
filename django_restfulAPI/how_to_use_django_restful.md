# how to use django-restful

## Serialization

序列器负责将数据`序列化`或`反序列化`。

### serializers.Serializer

### serializers.ModelSerializer

It's important to remember that ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:

- An automatically determined set of fields.
- Simple default implementations for the create() and update() methods.

`ModelSerializer`没有做额外的逻辑，只是创建序列化模型的捷径。其中包含自动生成的属性和默认的`create`和`update`

## Requests and Responses

### Requests

REST framework introduces a `Request` object that extends the regular `HttpRequest`, and provides more flexible request parsing. __The core functionality of the Request object is the `request.data` attribute, which is similar to `request.POST`, but more useful for working with Web APIs.__

```py
request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
```

### Responses

REST framework also introduces a `Response` object, which is a type of `TemplateResponse` that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.

```py
return Response(data)  # Renders to content type as requested by the client.
```

### Wrapping API views

`rest_framework`提供了两种方法实现`API view`

The `@api_view` decorator for working with function based views.

The `APIView` class for working with class-based views.

some mixins

- ListModelMixin
- CreateModelMixin
- RetrieveModelMixin
- UpdateModelMixin
- DestroyModelMixin

some genericAPIView

- ListCreateAPIView
- RetrieveUpdateDestroyAPIView

## Authentication and Permissions

对于APIView，直接添加`permission_class`

常见的权限类型`IsAuthenticatedOrReadOnly & IsAuthenticated & IsAdminUser`

如何增加对部分对象的权限

```py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
```

## Relationships & Hyperlinked APIs

### what is HyperlinkedModelSerializer

使用指向特定对象的`url`代替`id`。

The `HyperlinkedModelSerializer` has the following differences from `ModelSerializer`:

- It does not include the `id` field by default.
- It includes a `url` field, using `HyperlinkedIdentityField`.
- Relationships use `HyperlinkedRelatedField`, instead of `PrimaryKeyRelatedField`.

使用`HyperlinkedRelatedField`时需要确保为使用的路径增加别名

### 增加分页功能

在项目setting.py文件中增加下列代码。

```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## ViewSets & Routers

### 在`ViewSets`中增加自定义`endpoint`。（关键）

Notice that we've also used the `@action` decorator to create a custom action, named highlight. __This decorator can be used to add any custom endpoints that don't fit into the standard create/update/delete style.__

Custom actions which use the `@action` decorator will respond to `GET` requests by default. We can use the `methods` argument if we wanted an action that responded to `POST` requests.

__The URLs for custom actions by default depend on the method name itself.__ If you want to change the way url should be constructed, you can include `url_path` as a decorator keyword argument.

使用`@action`装饰器来自定义非创建、更新、删除功能的端点。默认响应`GET`方法，可通过`method`修改。默认路径为方法名，可通过`url_path`修改。
