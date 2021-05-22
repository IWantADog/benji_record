# Install Rust

## Installing rustup on Linux or macOS

$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

## Updating and Uninstalling

$ rustup update

$ rustup self uninstall

## Troubleshooting

$ rustc --version

## Compiling and Running Are Separate Steps

Before running a Rust program, you must compile it using the Rust compiler by entering the rustc command and passing it the name of your source file, like this:

> $ rustc main.rs

If you’re more familiar with a dynamic language, such as Ruby, Python, or JavaScript, you might not be used to compiling and running a program as separate steps. __Rust is an ahead-of-time compiled language, meaning you can compile a program and give the executable to someone else, and they can run it even without having Rust installed.__ If you give someone a .rb, .py, or .js file, they need to have a Ruby, Python, or JavaScript implementation installed (respectively). But in those languages, you only need one command to compile and run your program. Everything is a trade-off in language design.

> 通过`rustc`编译代码，生成可执行文件。编译之后的`rust`可以直接在其他机器上运行，不需要额外安装编译器。




