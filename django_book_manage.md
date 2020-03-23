# django book manage

## 2020.03.19

django图书管理系统v1.1.xmind

修改

1、管理员功能使用django自带的用户认证系统。具体的使用方法是，修改admin中的模版。

2、所有的view基于view class base， form基于ModelForm

3、着重关注用户的使用，新增以下功能:

- 添加用户评论功能。
- ~~对于book类增加位置信息。~~

4、增加社交功能，模仿微博的结构

5、在comment分支上尝试使用[Django “excontrib” Comments](https://django-contrib-comments.readthedocs.io/en/latest/)

## 2020.03.22

问题：在js中使用django的csrf_token

方法：
[Cross Site Request Forgery protection](https://docs.djangoproject.com/en/2.0/ref/csrf/#ajax)

# Django-Design-Patterns-and-Best-Practices阅读进度
https://github.com/cundi/Django-Design-Patterns-and-Best-Practices/blob/master/%E7%AC%AC%E5%85%AD%E7%AB%A0-admin%E6%8E%A5%E5%8F%A3.md