# Method Syntax

Methods are similar to functions: they’re declared with the fn keyword and their name, they can have parameters and a return value, and they contain some code that is run when they’re called from somewhere else. However, `methods` are different from `functions` in that they’re defined within the context of a struct, and their first parameter is always `self`, which represents the instance of the struct the method is being called on.

## Defining Methods

```rust
// struct and method
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

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

We’ve chosen `&self` here for the same reason we used `&Rectangle` in the function version: we don’t want to take ownership, and we just want to read the data in the struct, not write to it. If we wanted to change the instance that we’ve called the method on as part of what the method does, we’d use `&mut self` as the first parameter. __Having a method that takes ownership of the instance by using just self as the first parameter is rare; this technique is usually used when the method transforms self into something else and you want to prevent the caller from using the original instance after the transformation.__

> The main benefit of using _methods_ instead of _functions_, in addition to using method syntax and not having to repeat the type of self in every method’s signature, is for organization. We’ve put all the things we can do with an instance of a type in one _impl_ block rather than making future users of our code search for capabilities of _Rectangle_ in various places in the library we provide.

### Where’s the -> Operator?

> This automatic referencing behavior works because methods have a clear receiver—the type of self. Given the receiver and name of a method, Rust can figure out definitively whether the method is reading (&self), mutating (&mut self), or consuming (self). The fact that Rust makes borrowing implicit for method receivers is a big part of making ownership ergonomic in practice.

## Associated Functions

Another useful feature of `impl` blocks is that we’re allowed to define functions within `impl` blocks that don’t take self as a parameter. These are called _associated functions_ because they’re associated with the struct. They’re still functions, not methods, because they don’t have an instance of the struct to work with. You’ve already used the `String::from` associated function.

__Associated functions are often used for constructors that will return a new instance of the struct.__

To call this associated function, we use the `::` syntax with the struct name; `let sq = Rectangle::square(3);` is an example.

## Multiple impl Blocks

Each struct is allowed to have multiple `impl` blocks.
