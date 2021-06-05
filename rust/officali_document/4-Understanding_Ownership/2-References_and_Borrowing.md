# References and Borrowing

```rust
    let s1 = String::from("hello");

    let len = calculate_length(&s1)
```

`&s1`的形式创建了一个引用指向s1但是并不拥有s1的数据数据。所以当`&s1`超出作用域时，数据不会被`drop`。

这种像方法中传入一个引用，在rust中被称为`borrowing`。__不过在function中无法修改引用所指的数据__。如果尝试修改引用的数据，rust在编译时会报错。

## Mutable References

可变的引用。

```rust
fn main() {
    let mut s = String::from("hello");

    change(&mut s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

__不过对于某份数据，只能仅有一个可变引用。__ 如果存在多个可变引用指向同一份数据，rust在编译时会报错。

```rust
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;

    println!("{}, {}", r1, r2);
```

Note that a reference’s scope starts from where it is introduced and continues through the last time that reference is used

__一个引用的作用域是从它被引用到它最后一次被使用。__ 对于指向同一数据的可变引用和不可变引用的作用域不可重叠。

```rust
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{} and {}", r1, r2);
    // r1 and r2 are no longer used after this point

    let r3 = &mut s; // no problem
    println!("{}", r3);
```


