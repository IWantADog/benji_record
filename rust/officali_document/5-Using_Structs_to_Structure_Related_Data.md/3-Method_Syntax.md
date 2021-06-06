# Method Syntax

注意区分`method`和`function`的不同。

// todo 姑且下个结论，理解透彻后在回来修改

`method`一般与`struct`绑定。

## 定义`method`

```rust
// struct and method
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

// 如何定义method
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

定义`method`时，注意只读和可写引用的区别。对于只读取数据的`method`，传入`&self`；对于需要修改数据的`method`需要传入`&mut self`。也可仅传入`self`，使用时需要注意`ownership`。

## Associated Functions

`struct`中可以定义一种`Associated functions`，它的本质是`function`，而不是`method`。不过它普通的`function`也不相同，因为它和`struct`关联。

`associated function`定义是不需要包含`self`。

`associated function`通常用来创建一个结构体实例。

> 感觉类似于c中的构造方法或是python中的`__init__`

> String::from() 就是一个 `associated function`。


## Multiple impl Blocks

一个结构体可以有多个`impl`，这在语法上没有问题，不过在实现上并没有什么意义。