# Variables and Mutability

Mutability can be very useful. __Variables are immutable only by default__. You can make them mutable by adding `mut` in front of the variable name. In addition to allowing this value to change, mut conveys intent to future readers of the code by indicating that other parts of the code will be changing this variable’s value.

## Differences Between Variables and Constants

- Constants aren’t just immutable by default—they’re always immutable.

- Constants can be declared in any scope, including the global scope, which makes them useful for values that many parts of code need to know about.

- The last difference is that constants may be set only to a constant expression, not the result of a function call or any other value that could only be computed at runtime.

## Shadowing

Shadowing is different from marking a variable as `mut`, because we’ll get a compile-time error if we accidentally try to reassign to this variable without using the `let` keyword. By using `let`, we can perform a few transformations on a value but have the variable be immutable after those transformations have been completed.

The other difference between `mut` and shadowing is that because we’re effectively creating a new variable when we use the `let` keyword again, we can change the type of the value but reuse the same name.


https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html