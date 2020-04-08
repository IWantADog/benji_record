# Using JQuery Core

## Avoiding Conflicts with Other Libraries

### Create a New Alias

`jQuery.noConflict()`返回一个新的JQuery别名。

```js
<script src="prototype.js"></script>
<script src="jquery.js"></script>
<script>
 
// Give $ back to prototype.js; create new alias to jQuery.
var $jq = jQuery.noConflict();
 
</script>
```

### Use an Immediately Invoked Function Expression

通过立即调用的方式避免冲突，这种方式JQuery插件作者常用

```js
<!-- Using the $ inside an immediately-invoked function expression. -->
<script src="prototype.js"></script>
<script src="jquery.js"></script>
<script>
 
jQuery.noConflict();
 
(function( $ ) {
    // Your jQuery code here, using the $
})( jQuery );
 
</script>
```

### Use the Argument That's Passed to the jQuery( document ).ready() Function

将`$`作为产生传入，可以在函数中正常使用`$`。这种方式比较常用。

当jquery.js在可能发生冲突的其他js包之前引用时，`$`的含义会发生变化导致无法使用了，所以必须使用JQuery()。

```js
<script src="jquery.js"></script>
<script src="prototype.js"></script>
<script>
 
jQuery(document).ready(function( $ ) {
    // Your jQuery code here, using $ to refer to jQuery.
});
 
</script>
```

## Utility Methods

$.trim(): 去除两端多余空格

$.each(): 迭代。可以迭代数值、字典。

```js
$.each([ "foo", "bar", "baz" ], function( idx, val ) {
    console.log( "element " + idx + " is " + val );
});
 
$.each({ foo: "bar", baz: "bim" }, function( k, v ) {
    console.log( k + " : " + v );
});
```

$.inArray(): 返回指定元素的下标，如果不存在返回-1。

```js
var myArray = [ 1, 2, 3, 5 ];
 
if ( $.inArray( 4, myArray ) !== -1 ) {
    console.log( "found it!" );
}
```

$.extend(): 使用第二个字典的值，更新第一个字典中相同key对应的value。该方法会返回一个新字典，并且会修改第一字典。如果不像修改第一字典。这样使用`var newObject = $.extend( {}, firstObject, secondObject );`

## Iterating

### $.each() && .each()

$.each(): 无法迭代JQuery collection

.each(): 迭代JQuery collection

$.map() && .map()

## Using jQuery’s .index() Function

### .index() with No Arguments

返回选中对象位于其副对象的index

### .index() with a String Argument

.index(): 获取当前选中的第一个对象，在指定的对象中的index。

```html
<ul>
    <div class="test"></div>
    <li id="foo1">foo</li>
    <li id="bar1" class="test">bar</li>
    <li id="baz1">baz</li>
    <div class="test"></div>
</ul>
<div id="last"></div>
```

```js
var baz = $( "#baz1" );
console.log( "Index: " + baz.index( "li" )); // 2
// 返回 "baz1" 在所有的 "li" 中的index
```

### .index() with a jQuery Object Argument

返回右侧对象在左侧对象中的index

```js
var foo = $( "li" );
var baz = $( "#baz1" );
 
console.log( "Index: " + foo.index( baz ) );
```


