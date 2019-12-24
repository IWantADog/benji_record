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

.filter(): bom元素过，既可以通过选择符表达式，也可通过函数过滤。

.next(): 选择下一个最接近的同辈元素。.nextAll() 

.prev()  .prevAll()则相反。

.siblings(): 选取相同bom层级的所有其他元素，不包括本身。

.addBack(): 添加当前的元素。

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


## 2019.12.21

.off(): 移除事件绑定。

.one(): 只触发一次随后立即解绑。

.trigger(): 模仿用户操作，触发事件。

- trigger提供与on相同的简写方法，当使用这些方法不带参数时，结果将是触发操作而不是绑定行为。

parseFloat(): 在字符串中从左至右地查找一个浮点（十进制）数。

.hide() & .show() & .fadeIn() & .fadeOut() & .slideDown() & .slideUp()

.is(): 接收一个选择器表达式，然后用选择器来测试当前的JQuery对象。如果集合中至少有一个元素与选择符匹配，则返回true

### 强大的.animate()

- 动画排队效果：通过animate()连缀实现。
- 越过队列：queue
- 手工队列：.queue()

一组元素上的效果：

- 当在一个.animate()方法中以多个属性的方式应用时，是同时发生的。
- 当以方法连缀的形式应用时，时按顺序发生的（排队效果）--除非queue选项值为false

多组元素上的效果：

- 默认情况时同时发生的。
- 当在另一个效果方法或者在.queue()方法的回调函数中应用时，是按顺序发生的（排队效果）

[css absolute & relative](http://www.wpdfd.com/issues/78/absolutely_relative)

JQuery.outerWidth(): 获取容器的宽度。

由于DOM元素与html元素部分接口不同，所以attr和prop同时存在。

- 获取html属性: .attr(); removeAttr()
- 获取DOM属性: .prop()
- 对于操作表单控件(输入框、单选框、多选框)的值时，建议使用val()方法。

值回调

### DOM树操作

插入新元素

- .insertBefore(): 在现有元素外部、之前添加内容。
- .prependTo(): 在现有元素内部、之前添加内容。
- .appendTo(): 在现有元素内部、之后添加内容。
- .insertAfter: 在现有元素外部、之后添加内容。

反向插入方法

- before: insertBefore的反方法。
- append: appendTo的反方法。

> 反向插入方法可以接收一个函数作为参数，传入的参数会对每个目标调用，返回被插入的HTML字符串。

包装元素：.wrapAll()、.wrap()、.wrapInner()

> 使用说明：被包装元素.wrap(容器元素)

复制元素.clone()
> 默认情况下不会复制匹配元素或其后代元素中绑定的事件。不过可以通过clone(true)，连同事件一同复制。

#### 替换元素

.html()获取和设置元素的html

.text()获取纯文本文件，忽略所有的html标签。尔当通过text()设置文件是，html标签又会被正确转换。

.replaceAll() .replaceWith()

#### 清空元素

.empty():移除每个匹配的元素中的元素。

.remove() && .detach() : 从文档中移除每个匹配的元素及其后代元素，但不实际删除它们。


### ajax

.load()

$.getJSON()

$.each()

$.getScript():向页面注入脚本。

$(form).submit()

.serialize():作用与一个JQuery对象，将匹配的DOM元素转化为能够随Ajax请求传递的查询字符串。

#### 为ajax事件注册回调函数

$(document).ajaxStart(); $(document).ajaxStop()

### 事件委托

.on()

[同源策略](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy)


