# JQuery Event

## JQuery Event Basics

### Extending Events to New Page Elements

on只能向已经存在的元素绑定事件监听，对于绑定之后添加的元素不会绑定事件监听。

> It is important to note that .on() can only create event listeners on elements that exist at the time you set up the listeners. Similar elements created after the event listeners are established will not automatically pick up event behaviors you've set up previously.

不过可以通过事件委托的形式，处理新元素。[Understanding Event Delegation](https://learn.jquery.com/events/event-delegation/)

将事件绑定在更高一级的对象，on绑定事件时设置筛选器，对触发事件的对象进行筛选，只有指定类型的对象才可触发事件。这样当新子元素被添加后，依然可以触发事件。

> Event delegation allows us to attach a single event listener, to a parent element, that will fire for all descendants matching a selector, whether those descendants exist now or are added in the future.

### Inside the Event Handler Function

- pageX, pageY:点击时鼠标相对左上角的坐标

- type: 事件的类型

- which: 对于键盘和鼠标事件，which包含一个唯一映射，指向每个按键和鼠标左右键

- data: 事件绑定时传入的数据

- target: 事件初始化的DOM元素。

- currentTarget: 事件冒泡阶段当前的对象。与this指向的东西相同

- delegateTarget: 当时用事件委托时，指向委托对象。当没有事件委托时与currentTraget相同。

- namespace&timeStamp

- preventDefault(): 阻止元素的默认行为

- stopPropagation(): 阻止事件冒泡

### Setting Up Multiple Event Responses

绑定拥有相同处理逻辑的事件:

```js
// Multiple events, same handler
$( "input" ).on(
    "click change", // Bind handlers for multiple events
    function() {
        console.log( "An input was clicked or changed!" );
    }
);
```

不同事件绑定不同逻辑:

```js
// Binding multiple events with different handlers
$( "p" ).on({
    "click": function() { console.log( "clicked!" ); },
    "mouseover": function() { console.log( "hovered!" ); }
});
```

### Namespacing Events

事件的命名空间

```js
$( "p" ).on( "click.myNamespace", function() { /* ... */ } );
$( "p" ).off( "click.myNamespace" );
$( "p" ).off( ".myNamespace" );
```

### Tearing Down Event Listeners

关闭事件监听

移除指定类型的事件：

```js
$( "p" ).off( "click" );
```

如果拥有处理事件的函数名称，可以添加函数名，移除指定事件。

```js
var foo = function() { console.log( "foo" ); };
var bar = function() { console.log( "bar" ); };
$( "p" ).on( "click", foo ).on( "click", bar );
$( "p" ).off( "click", bar );// foo is still bound to the click event
```

### Setting Up Events to Run Only Once

绑定的事件只触发一次。事件在第一次触发后，不会从被绑定元素上移除。

```js
$( "p" ).one( "click", firstClick );
```


## Introduction To Events

> With this in mind, it's beneficial to use the on method because the others are all just syntactic sugar, and utilizing the on method is going to result in faster and more consistent code.

### Event delegation

Event delegation works because of the notion of event bubbling. For most events, whenever something occurs on a page (like an element is clicked), the event travels from the element it occurred on, up to its parent, then up to the parent's parent, and so on, until it reaches the root element, a.k.a. the window. So in our table example, whenever a td is clicked, its parent tr would also be notified of the click, the parent table would be notified, the body would be notified, and ultimately the window would be notified as well. While event bubbling and delegation work well, the delegating element (in our example, the table) should always be as close to the delegatees as possible so the event doesn't have to travel way up the DOM tree before its handler function is called.

The two main pros of event delegation over binding directly to an element (or set of elements) are performance and the aforementioned event bubbling. Imagine having a large table of 1,000 cells and binding to an event for each cell. That's 1,000 separate event handlers that the browser has to attach, even if they're all mapped to the same function. Instead of binding to each individual cell though, we could instead use delegation to listen for events that occur on the parent table and react accordingly. One event would be bound instead of 1,000, resulting in way better performance and memory management.

The event bubbling that occurs affords us the ability to add cells via Ajax for example, without having to bind events directly to those cells since the parent table is listening for clicks and is therefore notified of clicks on its children. If we weren't using delegation, we'd have to constantly bind events for every cell that's added which is not only a performance issue, but could also become a maintenance nightmare

### The event object

当需要同时调用`.preventDefault()`和`.stopPropagation()`时，可以通过`return false`的简洁方式实现。

## Triggering Event Handlers

对于绑定的事件，可以通过`.trigger()`手动触发。

不过`.trigger()`无法触发模拟本机浏览器的操作，例如点击文件上传标签和a标签。之所以不可以，是因为Jquery的事件系统中没有对应的事件。

不要过分使用`.trigger()`，普通方法的触发，应直接调用方法。

### How can I mimic a native browser event, if not .trigger()?

jquery.simulate.js是JQuery UI Team开发的用于触发浏览器本机事件的插件

#### .trigger() vs .triggerHandler()

[triggerHandler documentation](https://api.jquery.com/triggerHandler/)

There are four differences between .trigger() and .triggerHandler()

- .triggerHandler() only triggers the event on the first element of a jQuery object.
- .triggerHandler() cannot be chained. It returns the value that is returned by the last handler, not a jQuery object.
- .triggerHandler() will not cause the default behavior of the event (such as a form submission).
- Events triggered by .triggerHandler(), will not bubble up the DOM hierarchy. Only the handlers on the single element will fire.