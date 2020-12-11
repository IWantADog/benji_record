# Data Types

## Scalar Types

### Integer Types

Length | Signed   | Unsigned
-------|----------|---------
8-bit  |   i8     |   u8
16-bit |   i16    |   u16
32-bit |   i32    |   u32
64-bit |   i64    |   u64
128-bit|   i128   |   u128
arch   |   isize  |   usize

Additionally, the isize and usize types depend on the kind of computer your program is running on: 64 bits if you’re on a 64-bit architecture and 32 bits if you’re on a 32-bit architecture.

> Rust’s defaults are generally good choices, and __integer types default to i32__: this type is generally the fastest, even on 64-bit systems. The primary situation in which you’d use isize or usize is when indexing some sort of collection.

### Floating-Point Types

Rust’s floating-point types are `f32` and `f64`, which are 32 bits and 64 bits in size, respectively. __The default type is `f64`__.

### Numeric Operations

```rust
fn main() {
    // addition
    let sum = 5 + 10;

    // subtraction
    let difference = 95.5 - 4.3;

    // multiplication
    let product = 4 * 30;

    // division
    let quotient = 56.7 / 32.2;

    // remainder
    let remainder = 43 % 5;
}
```

### The Boolean Type

A Boolean type in Rust has two possible values: `true` and `false`. __Booleans are one byte in size.__ The Boolean type in Rust is specified using `bool`. For example:

```rust
fn main() {
    let t = true;

    let f: bool = false; // with explicit type annotation
}
```

### The Character Type

Rust’s `char` type is `four bytes` in size and represents a Unicode Scalar Value, which means it can represent a lot more than just ASCII.

## Compound Types

### The Tuple Type

A tuple is a general way of grouping together a number of values __with a variety of types__ into one compound type. __Tuples have a fixed length: once declared, they cannot grow or shrink in size.__

We create a tuple by writing a comma-separated list of values inside parentheses. Each position in the tuple has a type, and the types of the different values in the tuple don’t have to be the same. We’ve added optional type annotations in this example:

To get the individual values out of a tuple, we can use pattern matching to destructure a tuple value, like this:

```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {}", y);
}
```

In addition to destructuring through pattern matching, __we can access a tuple element directly by using a period (.) followed by the index of the value we want to access.__ For example:

```rust
fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

### The Array Type

__Unlike a tuple, every element of an array must have the same type__. Arrays in Rust are different from arrays in some other languages because __arrays in Rust have a fixed length__, like tuples.

You would write an array’s type by using square brackets, and within the brackets include the type of each element, a semicolon, and then the number of elements in the array, like so:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Writing an array’s type this way looks similar to an alternative syntax for initializing an array: if you want to create an array that contains the same value for each element, you can specify the initial value, followed by a semicolon, and then the length of the array in square brackets, as shown here:

```rust
let a = [3; 5];
```

### Accessing Array Elements

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];

    let first = a[0];
    let second = a[1];
}
```

### Invalid Array Element Access

The compilation didn’t produce any errors, but the program resulted in a runtime error and didn’t exit successfully. When you attempt to access an element using indexing, Rust will check that the index you’ve specified is less than the array length. If the index is greater than or equal to the array length, Rust will panic.
