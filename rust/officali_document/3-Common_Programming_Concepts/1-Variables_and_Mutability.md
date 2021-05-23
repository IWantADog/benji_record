# Variables and Mutability

Mutability can be very useful. __Variables are immutable only by default__. You can make them mutable by adding `mut` in front of the variable name. In addition to allowing this value to change, mut conveys intent to future readers of the code by indicating that other parts of the code will be changing this variable’s value.

> rust的变量默认是不可变的。对于修改不可变类型的操作，rust会在编译环节报错。

## Differences Between Variables and Constants

- 静态类型不能使用`mut`声明，静态类型默认是无法修改的。
- 使用`const`声明静态类型，而不是`let`。
- 静态类型必须是静态表达式，不能是方法或在运行是计算

## Shadowing

Rustaceans say that the first variable is `shadowed` by the second, which means that the second variable’s value is what appears when the variable is used.

> 当一个变量名被多次使用，ruster称前一个变量被后一个变量`shadowed`.

> `shadowing`的本质是重新声明了一个变量。和`mut`有本质的区别。

