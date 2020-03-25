# django development experience

[Django Design Patterns and Best Practices](https://github.com/cundi/Django-Design-Patterns-and-Best-Practices)

### 模型

因设计而规范，又因优化而非规范

用户账户

```python
class Profile(models.Model):
    user = models.OnToOneField(settings.AUTH_USER_MODEL, primary_key=True)
```

多个账户类型 [link](https://github.com/cundi/Django-Design-Patterns-and-Best-Practices/blob/master/%E7%AC%AC%E4%B8%89%E7%AB%A0-%E6%A8%A1%E5%9E%8B.md#%E5%A4%9A%E4%B8%AA%E8%B4%A6%E6%88%B7%E7%B1%BB%E5%9E%8B)

假设在应用中你需要几种类型的用户账户。这里需要有一个字段去跟踪用户使用的是哪一种账户类型。账户数据本身需要存储在独立的模型中，或者存储在一个统一的模型中。

建议使用聚合账户的办法，因为它能够改变账户类型而不丢失账户细节，兼具灵活性，最小化复杂性。此办法中，账户模型包含一个所有账户类型的字段超集。

### 模版

> 保证业务逻辑远离模板。

bootstrap: django-frontend-skeleton && django-bootstrap-toolkit

with ?

```
{% include "_navbar.html" with active_link='link2' %}
```

### admin 接口

修改admin登录页面的标题: `admin.site.site_header = "SuperBook Secret Area"`

admin的bootstrap主题: django-admin-bootstrapped

保护admin

1. 简单的方法：将admin的地址改为不太显眼的位置，例如`url(r'^secretarea/', include(admin.site.urls)),`

2. 一个稍微更加成熟的做法是在默认位置使用假的admin站点或者蜜罐（参见第三方包django-admin-honeypot）。不过，最好的选择对admin站点范围内使用HTTPS，因为常规的HTTP会把所有的数据以明文格式发送到网络中去。

django功能标识: gargoyle or django-waffle

### form

formset_factory

django-braces: 表单按照用户以不同的形式展示的简单解决方案。

SubscribeForm(prefix="offers") prefix是什么意思? [prefixes-for-forms](https://docs.djangoproject.com/en/3.0/ref/forms/api/#prefixes-for-forms)

[模式-一个视图的多个表单行为](https://github.com/cundi/Django-Design-Patterns-and-Best-Practices/blob/master/%E7%AC%AC%E4%B8%83%E7%AB%A0-%E8%A1%A8%E5%8D%95.md#%E6%A8%A1%E5%BC%8F-%E4%B8%80%E4%B8%AA%E8%A7%86%E5%9B%BE%E7%9A%84%E5%A4%9A%E4%B8%AA%E8%A1%A8%E5%8D%95%E8%A1%8C%E4%B8%BA)

### Other

django-command-extensions： 可视化模型关系

> If you can't measure it, you can't improve it.

django-debug-toolbar && django-silk: 分析后端性能

django-cache-machine && django-cachalot: django缓存框架

Varnish, a caching server that sits between your users and Django, many of your requests might not even hit the Django server.
