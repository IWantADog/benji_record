# References and Borrowing

When functions have references as parameters instead of the actual values, we won’t need to return the values in order to give back ownership, because we never had ownership.

We call having references as function parameters `borrowing`. As in real life, if a person owns something, you can borrow it from them. When you’re done, you have to give it back.

Just as variables are immutable by default, so are references. __We’re not allowed to modify something we have a reference to.__

## Mutable References

Mutable references have one big restriction: you can have only one `mutable reference` to a particular piece of data in a particular scope.

This code will fail:

```rust
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;

    println!("{}, {}", r1, r2);
```

The benefit of having this restriction is that Rust can prevent data races at compile time. A data race is similar to a race condition and happens when these three behaviors occur:

- Two or more pointers access the same data at the same time.
- At least one of the pointers is being used to write to the data.
- There’s no mechanism being used to synchronize access to the data.

As always, we can use curly brackets to create a new scope, allowing for multiple mutable references, just not simultaneous ones:

```rust
    let mut s = String::from("hello");

    {
        let r1 = &mut s;
    } // r1 goes out of scope here, so we can make a new reference with no problems.

    let r2 = &mut s;
```

__We also cannot have a mutable reference while we have an immutable one.__ Users of an immutable reference don’t expect the values to suddenly change out from under them! However, __multiple immutable references are okay__ because no one who is just reading the data has the ability to affect anyone else’s reading of the data

__Note that a reference’s scope starts from where it is introduced and continues through the last time that reference is used.__ For instance, this code will compile because the last usage of the immutable references occurs before the mutable reference is introduced:

```rust
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{} and {}", r1, r2);
    // r1 and r2 are no longer used after this point

    let r3 = &mut s; // no problem
    println!("{}", r3);
```

## Dangling References

In Rust, by contrast, the compiler guarantees that references will never be dangling references: if you have a reference to some data, the compiler will ensure that the data will not go out of scope before the reference to the data does.
