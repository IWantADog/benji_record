# JQuery Tips

该文件主要记载JQuery的一些零碎知识。

### window.onload与$(document).ready()的细微差别 TODO

`window.onload`当文档完全加载到浏览器中时被触发。而通过`$(document).ready()`注册的方法，会在DOM完全就绪时被调用。

这意味着当页面中有大量图片时，每副图片加载完成后才会执行`window.onload`，这样如果有事件需要绑定倒元素时，会出现意想不到的问题。而使用`ready`则可以更早的绑定事件。

不过使用`ready`时由于文件还未完全加载完成，所以有些信息也无法拿到。

`window.onload`每次只能绑定一个函数，而`$(document).ready()`可以绑定任意数量的函数，而且函数会按照绑定顺序执行。

### toggleClass()：两种状态切换

### .hover()

`.hover()`接收两个函数，第一个函数在鼠标进入被选择的元素时执行，第二个函数在鼠标离开该元素时触发。

### .is()

接收一个选择器表达式，然后用选择器来测试当前的JQuery对象。如果集合中至少有一个元素与选择符匹配，则返回true

### JQuery.outerWidth(): 获取容器的宽度。

### attr与prop

由于DOM元素与html元素部分接口不同，所以attr和prop同时存在。

- 获取html属性: .attr(); removeAttr()
- 获取DOM属性: .prop()
- 对于操作表单控件(输入框、单选框、多选框)的值时，建议使用val()方法。

### 值回调：就是给参数传入一个函数，而不是一个具体的值。
