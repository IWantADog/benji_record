# Functions

## Function Parameters

rust的方法定义是需要显式规定传入参数的类型。

## Function Bodies Contain Statements and Expressions

statements不返回值；expressions返回值。

> 注意区分`statements`和`expressions`。注意区分有分号和没有分号的情况。

## Functions with Return Values

rust 可以通过`->`指明返回的数据类型。


```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();

    println!("The value of x is: {}", x);
}
```