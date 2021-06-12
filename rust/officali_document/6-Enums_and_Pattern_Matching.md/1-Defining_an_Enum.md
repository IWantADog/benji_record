# Enum

rust的枚举类型。

```rust
enum Status {
    RUNNING: String,
    FAIL: String,
}
```

rust的枚举类型，可以选择是否指定项类型。同时枚举类型中的项支持各种类型，例如`strings`、`numeric`、`struct`。

rust的enum类型和structs和相似。也可以在enum上定义`impl`。

rust中使用另一种方式实现null。

```rust
// <T> 先暂时简单的理解为任何对象
enum Option<T> {
    Some(T),
    None,
}
```

```rust
// how to use
let some_number = Some(5);
let some_string = Some("a string");

let absent_number: Option<i32> = None;
```

对于`Some`不用指定变量类型。对于`Option`需要指定变量类型，因为解释器无法从`None`判断数据类型。


`Option<T>`和`T`不能直接进行运算，因为他们是不同的类型，不正确的使用会在编译时报错。使用`Option<T>`时，用户必须显式将`Option<T>`转换为`T`。而转换时如果变量为null，需要相应的逻辑进行处理。

而对于没有声明为`Option`的变量，则可以假设变量不会为null，放心地使用。