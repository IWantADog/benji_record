# Functions

## Function Parameters

__In function signatures, you must declare the type of each parameter.__ This is a deliberate decision in Rust’s design: requiring type annotations in function definitions means the compiler almost never needs you to use them elsewhere in the code to figure out what you mean.

## Function Bodies Contain Statements and Expressions

Rust is an expression-based language.

Statements do not return values. Therefore, you can’t assign a let statement to another variable, as the following code tries to do; you’ll get an error:

```rust
//  In those languages, you can write x = y = 6 and have both x and y have the value 6; that is not the case in Rust.

fn main() {
    let x = (let y = 6);
}
```

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
