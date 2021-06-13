# Concise Control Flow with if let

// todo

感觉没办法理解。

```rust
fn test_if_let(){
    let some_u8_value = Some(0u8);
    match some_u8_value {
        Some(3) => println!("three"),
        _ => (),
    }

    // 这两个是等价的

    let some_u8_value1 = Some(0u8);
    if let Some(3) = some_u8_value1 {
        println!("three");
    }
}
```·、