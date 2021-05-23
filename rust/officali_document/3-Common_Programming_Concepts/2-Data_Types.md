# Data Types

rust是静态，强类型语言

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

Each signed variant can store numbers from `-(2**n - 1) to 2**（n - 1） - 1` inclusive, where n is the number of bits that variant uses. So an `i8` can store numbers from -(27) to 27 - 1, which equals -128 to 127. Unsigned variants can store numbers from 0 to 2n - 1, so a u8 can store numbers from 0 to 28 - 1, which equals 0 to 255.

> integer类型可以显式指定数据使用的位数。

> `isize` & `usize`的大小依赖于机器是64位还是32位。

> rust默认的integer的类型是`i32`，这是个通用的选择。

> 对于`isize` & `usize`的主要使用情况是为某种集合索引时

#### integer overflow

rust对于类型溢出的处理情况


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

> tuple可以容纳不同类型的数据。tuple有固定的长度，一旦声明，不能增加或缩减。

```rust
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```

> tuple支持和`python`类似的解包操作。

```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {}", y);
}
```

> 如果想只获取tuple的指定位置的数据，可以使用`.`来指定下标。

```rust
fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

### The Array Type

rust中的数组只能容纳同一类型的数据。并且数据是定长的。

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

```rust
let a = [3; 5];
a = [3,3,3,3,3]
```

对于变长的数据需要使用vector

### Accessing Array Elements

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];

    let first = a[0];
    let second = a[1];
}
```

### Invalid Array Element Access

对于数组过界问题，rust编译可以通过。但会在运行是报错，不会像`c`访问不属于数据的内存。