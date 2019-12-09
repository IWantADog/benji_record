# 杂项
__一些问题记录。按记录时间先后排序__

[How do I include a JavaScript file in another JavaScript file?](https://stackoverflow.com/questions/950087/how-do-i-include-a-javascript-file-in-another-javascript-file)

[Dynamically load JS inside JS [duplicate]](https://stackoverflow.com/questions/14521108/dynamically-load-js-inside-js)

这两个都是一个问题。

这个问题是我尝试在odoo中调用百度地图api的时候出现的。当我将script标签加入head后，调用对象时一直会报对象未声明的错，开始我以为是odoo的问题，走了很多弯路。最后觉得可能是js未加载完成导致的，搜了一下就发现了这个问题。

----

### 2019.12.08 记录

问题

odoo10有tree视图点击进入form视图，之后点击浏览器回退按钮，页面回退到分页为1的页面。


~~从form视图回退到tree视图的问题是，ListView.Group.view可能丢失了或是被修改了。~~

情况记录

- 当从form视图回退到tree视图，点击第一次时会先推到分页为1的页面，但点击第二次时就会返回到正确的页面。

猜想：

1. ~~当点击tree视图某条数据时，js向history中压入了某条数据。~~ 未发现向history中压入数据的逻辑。

2. ListView.Group中view被修改。ListView.Group中view为唯一，当渲染之后就被丢弃。所以当点击回退按钮时，js新创建了一个页面。

最终解决办法：

在list_view.js中维护一个全局变量emp_current_min，用以记录每个model的上一次current_min。emp_current_min字典，键值对为`model:current_min`

当点击tree中的某一行时，在emp_current_min中创建键值对。

当执行`render_dataset`获取current_min时先在emp_current_min中搜索是否存在该model，若存在将this.current_min置为value并从emp_current_min中删除，且`current_min_key=true`；若不存在则跳过。

在接下来的逻辑中，若`current_min_key=true`则取this.current_min;反之则取view.current_min。

最后将`this.current_min_key=false`。

```javascript
if (this.view.model in emp_current_min){
    this.current_min_key = true;
    this.current_min = emp_current_min[this.view.model];
    delete emp_current_min[this.view.model];
}

//var current_min = this.datagroup.openable ? this.current_min : view.current_min; //源码
var current_min = this.current_min_key ? this.current_min : view.current_min;
this.current_min_key = false;

```

----