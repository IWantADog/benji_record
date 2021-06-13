# The match Control Flow Operator

how to use

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => {
            println("this is Quarter");
            return 25;
        },
    }
}
```

`match`支持对枚举类型的嵌套进行解构。

```rust
enum  VEGETABLE {
    TOMATO,
    P0TATO,
}

enum FOOD {
    APPLE,
    PEACH,
    VEG(VEGETABLE),
}
```

`match`会对枚举类型进行检测，发现有未处理的枚举类型型，在代码编译时会提醒用户。


`_` placeholder(占位符)：对于不需要处理的状态，可以使用占位符统一捕获。
