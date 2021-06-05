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


## Ownership Rules

First, let’s take a look at the ownership rules. Keep these rules in mind as we work through the examples that illustrate them:

- Each value in Rust has a variable that’s called its owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.

    > Rust calls drop automatically at the closing curly bracket.

## Variable Scope

### Ways Variables and Data Interact: Move

```rust
// how to understand move
    let s1 = String::from("hello");
    let s2 = s1;

    println!("{}, world!", s1);
```
s1 & s2实质为`存储在stack中包含指向实际存储数据的结构体`，而`hello`存储在heap中。当把s1赋为s2，本质是将结构体的数据赋给为s2，heap中的数据没有被修改。

如果出现这种情况，在回收内存是会同时对s1和s2都执行回收操作。但执行两次回收会出现内存问题并容易收到攻击。

rust对于这种情况的对策是，当将s1赋为s2，s1便失效了，在s2被创建之后在使用s1会在编译环节报错。这样在最后触发内存回收时，只会回收内存一次。

对于将s2赋为s1，并且之后s1失效，被成为`s1 be moved into s2`。


### Ways Variables and Data Interact: Clone

想要复制不仅包含stask中的指针结构体，还包括heap中的实际数据，需要通过`clone`。

```rust
 let s1 = String::from("hello");
    let s2 = s1.clone();

    println!("s1 = {}, s2 = {}", s1, s2);
```

### Stack-Only Data: Copy

对于像`int`类型在编译是有固定内存的数据，只会存储在`stack`中。所以普通的赋值就创建了新的数据。

```rust
    let x = 5;
    let y = x;

    println!("x = {}, y = {}", x, y);
```

类似的数据还有：

- All the integer types, such as u32.
- The Boolean type, bool, with values true and false.
- All the floating point types, such as f64.
- The character type, char.
- Tuples, if they only contain types that are also Copy. For example, (i32, i32) is Copy, but (i32, String) is not.

## Ownership and Functions

The ownership of a variable follows the same pattern every time: __assigning a value to another variable moves it. When a variable that includes data on the heap goes out of scope, the value will be cleaned up by drop unless the data has been moved to be owned by another variable.__

