# django development experience

## Django Design Patterns and Best Practices

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



## 阅读进度

https://github.com/cundi/Django-Design-Patterns-and-Best-Practices/blob/master/%E7%AC%AC%E5%85%AB%E7%AB%A0-%E5%A4%84%E7%90%86%E6%97%A7%E7%89%88%E6%9C%AC%E4%BB%A3%E7%A0%81.md