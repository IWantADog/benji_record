# Defining and Instantiating Structs

## 结构体定义以及初始化

```rust
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// how to use
let user1 = User {
    email: String::from("someone@example.com"),
    username: String::from("someusername123"),
    active: true,
    sign_in_count: 1,
};

user1.email = String::from("anotheremail@example.com");
```

## 初始化`struct`的简略写法。

```rust
fn build_user(email: String, username: String) -> User {
    User {
        email: email,
        username: username,
        active: true,
        sign_in_count: 1,
    }
}

fn build_user(email: String, username: String) -> User {
    User {
        email, // 省略写法
        username, // 省略写法
        active: true,
        sign_in_count: 1,
    }
}
```

## 结构体的简略复用方式 

```rust
    let user2 = User {
        email: String::from("another@example.com"),
        username: String::from("anotherusername567"),
        active: user1.active,
        sign_in_count: user1.sign_in_count,
    };

    let user2 = User {
        email: String::from("another@example.com"),
        username: String::from("anotherusername567"),
        ..user1
    };
```

`..`对于未显式指定的项，使用旧值；显式指定的项使用新值。

## 使用不指定键名的`struct`

```rust
    struct Color(i32, i32, i32);
```

类似上述的结构体在rust中被称为`tuple struct`。
- 不同的结构体即使拥有相同数据类型的项，也被视为完全不同的结构体。
- 通过`.1`的格式访问结构体的数据。

```rust
struct Point(i32, i32, i32);

    let point = Point(1,2,3);
    println!("{} {} {}", point.0, point.1, point.2);
}
```








