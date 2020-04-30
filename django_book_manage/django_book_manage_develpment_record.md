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

## 2020.04.04

1. 实现django-comment-xtd的全部形式 ✅

2. 研究django-comment-xtd的源码

3. 搞清楚模版中tag的使用方式，并在master分支上实验。

4. 手动实现模版嵌套，及tag开发法工作。

5. ~~尝试使用js html模版，渲染前端页面~~。采用直接将html整体穿回传的办法。

6. 实现回复的评论。✅

7. 新增评论后整体刷新所有评论。✅

## 2020.04.07

1. 页面美化，方法重构
    - css position [link](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position)
    - css selector

2. 研究django-comment-xtd的源码

## 2020.04.09

django restfult api

前端框架 vue

数据库设计