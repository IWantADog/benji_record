# django book manage 想法及功能记录

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

## 2020.03.25

1、评论的分页，使用js的分页 [Pagination.js](https://pagination.js.org/)

2、回复评论的页面格式设计

3、like功能

4、django class base view的常用字段方法总结
