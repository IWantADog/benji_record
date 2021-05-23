# Functions

## Function Parameters

rust的方法定义是需要显式规定传入参数的类型。

## Function Bodies Contain Statements and Expressions

statements不返回值；expressions返回值。

> 注意区分`statements`和`expressions`

# keep going
https://doc.rust-lang.org/book/ch03-03-how-functions-work.html#functions-with-return-values

__Expressions__ do not include ending semicolons. If you add a semicolon to the end of an expression, you turn it into a __statement__, which will then not return a value.

## Functions with Return Values

Rust don’t name return values, but we do declare their type after an arrow `(->)`.

You can return early from a function by using the `return` keyword and specifying a value, __but most functions return the last expression implicitly__.

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();

    println!("The value of x is: {}", x);
}
```
