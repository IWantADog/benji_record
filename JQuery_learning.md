# JQuery 学习记录

[官方参考文档](http://api.jquery.com)

## 2019.12.17

### css选择器、css伪类?

```javascript
$('tr:even').addClass('alt');
$('tr:nth-child(odd)').addClass('alt');
```

:contains()选择器

:input 输入字段、文本区、选择列表和按钮元素

:button 按钮元素或type属性值为button的输入元素

:enabled 启用的表单元素

:disabled 禁用的表单元素

:checked 勾选的单选按钮或复选框

:selected 选择的选项元素

## bom遍历方法

.filter()

.next() .nextAll() .prev()  .prevAll()  .siblings()

.addBack()

## 访问DOM元素

所有选择符表达式和多数JQuery方法都返回一个JQuery元素。但对于想要直接访问DOM元素的情况，JQuery提供了.get()方法。不过为了进一步简化代码可以通过下标索引的形式访问。

```javascript
var myTag = $('#my-div').get(0).tagName
// 等价于
var myTag = $('#my-div')[0].tagName
```

## 2019.12.18

### window.onload与$(document).ready()的细微差别

### JQuery隐式迭代机制

toggleClass()

### event详细信息[链接](http://api.jquery.com/category/events/event-object)


