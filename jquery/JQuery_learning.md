# JQuery 学习记录

[官方参考文档](http://api.jquery.com)

## JQuery选择与筛选

[css选择器-阮一峰](http://www.ruanyifeng.com/blog/2009/03/css_selectors.html) 
[css选择器-MDN](https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Getting_started/Selectors)

#### css伪类

实用的JQuery自定义选择器。:odd代表奇数行、:even代表偶数行、:eq(n)选择第n行。
>ps:选择符从0开始计数，第一个为0为偶数

:nth-child()根据元素的父元素而非当前选择元素的所有元素来计算位置，它可接收数值、odd、even。
>ps:`:nth-child()`是JQuery中唯一从1开始计数的选择器。

```javascript
$('tr:even').addClass('alt');
$('tr:nth-child(odd)').addClass('alt');
```

一些伪类选择器
选择符            | 匹配
-----------------| --------------------
:contains(heart) | 选择存在heart文本的元素
:input           | 输入字段、文本区、选择列表和按钮元素
:button          | 按钮元素或type属性值为button的输入元素
:enabled         | 启用的表单元素
:disabled        | 禁用的表单元素
:checked         | 勾选的单选按钮或复选框
:selected        | 选择的选项元素

### bom遍历方法

获取元素的父、子、兄弟节点
方法名            | 功能
-----------------|----------------------
JQuery.filter()  | bom元素过滤，既可以通过选择符表达式，也可通过函数过滤。
JQuery.next()、.nextAll() | 选择下一个最接近的同辈元素。
JQuery.prev()、.prevAll() | 选择上一个最接近的同辈元素。
JQuery.siblings()| 选取相同bom层级的所有其他元素，不包括本身。
JQuery.addBack() | 添加当前的元素。

## 访问DOM元素

所有选择符表达式和多数JQuery方法都返回一个JQuery元素。但对于想要直接访问DOM元素的情况，JQuery提供了.get()方法。不过为了进一步简化代码可以通过下标索引的形式访问。

```javascript
var myTag = $('#my-div').get(0).tagName
// 等价于
var myTag = $('#my-div')[0].tagName
```

## 高级选择符和遍历

[所有选择器符介绍](http://api.jquery.com/category/selectors)
[遍历方法介绍](http://api.jquery.com/category/traversing)

## JQuery隐式迭代机制、JQuery行为队列机制

JQuery隐式迭代机制: 遍历数组中的元素。通过筛选器中this绑定的是DOM对象

JQuery的行为队列机制：JQuery按照事件的注册顺序触发事件。

## event详细信息 [链接](http://api.jquery.com/category/events/event-object)

## 事件的旅程

事件捕获：允许多个元素响应单击事件。在事件捕获的过程中，事件首先会交给最外层的元素，接着再交给更具体的元素。

事件冒泡：当事件发生时会首先发送给最具体的元素，在这个元素获得响应机会后，事件会向上冒泡到更一般的元素。

最终出台的DOM标准规定应同时使用这两种策略：首先，事件要从一般元素到具体元素逐层捕获，然后，事件再通过冒泡返回DOM树的顶层。

JQuery会在模型的冒泡阶段注册事件处理程序。

event.stopPropagation()阻止事件继续冒泡。

evnet.preventDefault()在触发默认操作之前终止事件。

## JQuery事件

.off(): 移除事件绑定。

.one(): 只触发一次随后立即解绑。

.trigger(): 模仿用户操作，触发事件。

- trigger提供与on相同的简写方法，当使用这些方法不带参数时，结果将是触发操作而不是绑定行为。

parseFloat(): 在字符串中从左至右地查找一个浮点（十进制）数。

## JQuery样式及动画

### 获取css

参数                | 功能
------------------ | ----------
.css('porperty')   | 获取单一属性组
.css(['porperty1', 'porperty2']) | 获取多个属性组
.css('porperty', value) | 设置单一属性值
.css({p1: v1, p2: v2'}) | 设置多个属性值

### .hide() & .show() & .fadeIn() & .fadeOut() & .slideDown() & .slideUp()

隐藏、显示、淡入、淡出、滑下、滑上。

以上所有的方法都可指定时长，效果会在指定的时间段中发生。系统预设两种速度参数：short、fast

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

### [css absolute & relative](http://www.wpdfd.com/issues/78/absolutely_relative)

## DOM树操作

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

.text()获取纯文本文件，忽略所有的html标签。而当通过text()设置文件是，html标签又会被正确转换。

.replaceAll() .replaceWith()

#### 清空元素

.empty(): 清除选中元素的内容，但保留该元素。

.remove() : 直接删除选中的元素。

.detach() : 从文档中分离匹配的元素，并返回（selection），并且包含绑定的事件。

## ajax

ajax不仅可以用来接送json，还可以获取html和xml

.load()

$.getJSON()

$.each()

$.getScript():向页面注入脚本。

$(form).submit()

.serialize():作用与一个JQuery对象，将匹配的DOM元素转化为能够随Ajax请求传递的查询字符串。

### 为ajax事件注册回调函数

$(document).ajaxStart(); $(document).ajaxStop()

### 事件委托 .on()

[同源策略](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy)

[Cross-Origin Resource Sharing]()

[同源策略-阮一峰](https://www.ruanyifeng.com/blog/2016/04/same-origin-policy.html)

[JSONP技术](https://zh.wikipedia.org/wiki/JSONP)：让用户通过script元素注入的方式绕开同源策略

$.ajaxSetup(): 修改调用ajax方法时每个选项的默认值，除非明确覆盖。

### 部分加载HTML页面

- .load()

## jquery plugin

[The JQuery Pligin Registry](http://plugins.jquery.com)

[JQuery plugin help](http://forum.jquery.com/using-jquery-plugins)

缓动函数

[JQuery UI 演示](https://jqueryui.com/effect/)

交互组件：resizable、Draggable、Droppable、Sortable

部件：Datepicker、Dialog、Tabs、Accordion

JQuery UI 主题卷轴：ThemeRoller

### :visible与:hidden

visible: 筛选所有未被隐藏的元素。hidden: 筛选所有被隐藏的元素。

.on(): [委托方法](https://api.jquery.com/on/)

.closest(): 该方法沿DOM树向上一层层移动，直至找到与给定的选择符表达式相匹配的元素。如果没有找到这个元素，那它就会返回一个”空的“JQuery对象。

### IIFE Immediately Invoked Function Expression

```javascript
(function($){
    // code
})(JQuery);
```

document元素是随着页面加载几乎立刻就可以调用的，所以把处理程序绑定到document上不需要等到完整的DOM构建完成。

element.scrollTop():[link](https://developer.mozilla.org/zh-CN/docs/Web/API/Element/scrollTop)

## 节流事件:

setInterval(): javascript方法可按照指定的周期（以毫秒计）来调用函数或计算表达式。

setTimeout(): javascript方法用于在指定的毫秒数后调用函数或计算表达式。

## 扩展事件

诸如mouseenter和ready这样的事件，都是JQuery中的特殊事件。

为了实现一个自定义事件，需要为`$.event.special`对象添加属性。这个属性的键是事件的名称，而它的值本身是一个对象。这个特殊的事件对象包含可在不同时刻调用的回调函数。

1. add会在每次为当前事件绑定处理程序是调用。
2. remove会在每次为当前事件删除处理程序是调用
3. setup会在为当前事件绑定处理程序，__且没有为元素的这个事件绑定其他处理程序是调用__。
4. teardown是setup的反操作，会在某个元素删除这个事件的最后一个处理程序时调用。
5. _default是当前事件的默认行为，在没有被事件处理程序阻止的情况下会执行。

## 高级效果

### 观察及终止动画

1. :animated：JQuery自定义选择符，用于检测元素是否处于动画的过程中。
2. stop(): 中止当前正在执行的过程，立即完成当前的动画。[link](https://api.jquery.com/stop/)
3. finish(): 与stop(true, true)类似，不过它也会使所有排队的动画都跳到各自完成的最终值。

### 动画全局效果属性

1. $.fn。关闭所有的动画效果`$.fx.off=true`
2. 定义效果时长。`$.fx.speed`。speed为jquery默认的速度，可以任意扩展。
    ```javascript
    speend: {
        slow: 600,
        fast: 200,
        _default: 400
    }
    ```

3. 缓动函数：用于控制jquery中动画效果在执行时的速度。[link](https://api.jquery.com/animate/)
    > The remaining parameter of .animate() is a string naming an easing function to use. An easing function specifies the speed at which the animation progresses at different points within the animation.__The only easing implementations in the jQuery library are the default, called swing, and one that progresses at a constant pace, called linear.__ More easing functions are available with the use of plug-ins, most notably the jQuery UI suite.

### 使用延迟对象

$.Deferred()、.resolve()、.reject()

每个延迟对象都会向其他代码承诺(promise)提供数据。这个承诺以另一个对象的形式来兑现，这个对象也有自己的一套方法。对于任何延迟对象，调用它的.promise()方法就可以取得其承诺对象。然后，通过调用这个承诺对象的各种方法，就可以添加在各种承诺兑现时调用的处理程序。

承诺对象相关的方法:

- .done(): 通过done添加的处理程序会在延迟对象被成功解决之后调用。

- .fail():处理程序会在延迟对象被拒绝之后调用。

- .always(): 处理程序在延迟对象完成其任务(无论解决或拒绝)时调用。

$.extend(): 融合多个对象到第一个对象，可以设置递归。[link](https://api.jquery.com/jquery.extend/)

### 精细地控制动画 step && progress

step函数大约每13毫秒会针对每个动画属性被调用一次。

progress函数在动画的生命周期中会被多次调用。它与step()的区别在于，它只会在动画的每一步针对每个元素被调用一次，与多少属性产生动画效果无关。它提供了动画其他方面的调整选项，包括动画的承诺对象、进度（0到1之间的一个值）和动画剩余的毫秒数。

JQuery动画系统最底层的方法是$.Animation()和$.Tween（）

[html data-*](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Global_attributes/data-*)
[data](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes)

### jquery模版系统

[Mustache](github.com/janl/mustache.js)  [Handlebars](handlebarsjs.com/)

## 高级ajax

### 处理ajax错误

jqXHR对象：JQuery中所有的ajax都会返回jqXHR对象。

通过jqXHR.status属性获取服务器返回错误的类型。

发送ajax请求时通过timeout设置请求的超时时间。

jqXHR对象

方法 | 功能
--- | ----
responseText or responseXMl | 返回包含的数据
status and statusText       | 返回状态码和状态描述
setRequestHeader            | 返回请求的header
abort                       | 提前中止通讯

ajax.always:在请求期间添加一个加载指示器，而在请求完成时或在其他情况下隐藏它。

clearTimeout: 取消由setTimeout设置的timeout

### ajax扩展功能--数据类型转换器

要定义一种新的ajax数据类型，需要给$.ajaxSetup()传递三个参数，acceptes、contents和converters。

其中，accpets属性会添加发送到服务器的头部信息，声明脚本可以理解的特定MIME类型；contents属性处理数据交换的另一方，它提供一个与响应的MIME类型进行匹配的正则表达式，以尝试自动检测这个元数据当中的数据类型。

### ajax预过滤器

预过滤器会在发送请求之前对请求进行过滤。

预过滤器会在$.ajax()修改或使用它的任何选项之前调用，因此通过预过滤器可以修改这些选项或基于新的、自定义选项发送请求。