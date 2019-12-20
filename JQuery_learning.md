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


.hover()


### 事件的旅程

事件捕获：允许多个元素响应单击事件。在事件捕获的过程中，事件首先会交给最外层的元素，接着再交给更具体的元素。

事件冒泡：当事件发生时会首先发送给最具体的元素，在这个元素获得响应机会后，事件会向上冒泡到更一般的元素。

最终出台的DOM标准规定应同时使用这两种策略：首先，事件要从一般元素到具体元素逐层捕获，然后，事件再通过冒泡返回DOM树的顶层。

JQuery会在模型的冒泡阶段注册事件处理程序。

event.stopPropagation()阻止事件继续冒泡。

evnet.preventDefault()在触发默认操作之前终止事件。




