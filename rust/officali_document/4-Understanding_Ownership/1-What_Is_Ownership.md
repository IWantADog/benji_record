# What is Ownership

`Ownership`是`rust`特有的概念。它保证了rust在没有垃圾回收机制的情况下的内存的分配安全。

__memory is managed through a system of ownership with a set of rules that the compiler checks at compile time. None of the ownership features slow down your program while it’s running.__

## heap and stack

stack:
- 栈中的数据大小都是固定的。
- 先入后出

heap:
- 堆中的数据没有顺序。
- 堆中的数据大小不是固定的。
- 对于新进入堆中的数据，必须先找到一个合适大小的数据块，然后将它标记为使用中，最后返回一个指向该地址的指针。

stack和heap的相比。从stack中寻找数据快于heap。因为stack的新数据都存在栈顶，而heap需要跟随指针才能找到数据块。

[keep reading](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html#what-is-ownership)

## Ownership Rules

First, let’s take a look at the ownership rules. Keep these rules in mind as we work through the examples that illustrate them:

- Each value in Rust has a variable that’s called its owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.

## Variable Scope

### Ways Variables and Data Interact: Move

```rust
// how to understand move
    let s1 = String::from("hello");
    let s2 = s1;

    println!("{}, world!", s1);
```


### Ways Variables and Data Interact: Clone

```rust
 let s1 = String::from("hello");
    let s2 = s1.clone();

    println!("s1 = {}, s2 = {}", s1, s2);
```

### Stack-Only Data: Copy

```rust
    let x = 5;
    let y = x;

    println!("x = {}, y = {}", x, y);
```

The reason is that types such as integers that have a known size at compile time are stored entirely on the stack, so copies of the actual values are quick to make. That means there’s no reason we would want to prevent x from being valid after we create the variable y. In other words, there’s no difference between deep and shallow copying here, so calling clone wouldn’t do anything different from the usual shallow copying and we can leave it out.

Rust has a special annotation called the `Copy` trait that we can place on types like integers that are stored on the stack.

Here are some of the types that are Copy:

- All the integer types, such as u32.
- The Boolean type, bool, with values true and false.
- All the floating point types, such as f64.
- The character type, char.
- Tuples, if they only contain types that are also Copy. For example, (i32, i32) is Copy, but (i32, String) is not.

## Ownership and Functions

The semantics for passing a value to a function are similar to those for assigning a value to a variable. Passing a variable to a function will move or copy, just as assignment does.



