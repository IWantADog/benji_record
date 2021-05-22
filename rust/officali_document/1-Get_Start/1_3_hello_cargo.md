# hello cargo

Cargo is Rust’s build system and package manager. Most Rustaceans use this tool to manage their Rust projects because Cargo handles a lot of tasks for you, such as building your code, downloading the libraries your code depends on, and building those libraries. (We call libraries your code needs dependencies.)

> `Cargo`是Rust的包管理工具。使用它来打包项目，安装依赖。

## Creating a Project with Cargo

$ cargo new hello_cargo

> 通过`cargo new project_name`创建新项目。新创建的项目包含一个`Cargo.toml`和包含`main.rs`的`src`文件夹。


## Building and Running a Cargo Project

cargo build

> 在项目文件夹下，运行`cargo build`会创建一个`./target/debug/xxx`文件，用于项目调试。

> 第一次运行build，会创建一个`Cargo.lock`文件。该文件用于跟踪项目依赖信息，由cargo自动维护，不需要手动维护。

cargo run

编译项目后直接运行。

cargo check

检测项目代码，是否存在错误。但是不会生成可执行文件，所以`check`快于`build`

## Building for Release

cargo build --release

__This command will create an executable in target/release instead of target/debug. The optimizations make your Rust code run faster, but turning them on lengthens the time it takes for your program to compile.__

> 运行该命令，在`target/debug`下生成可执行文件，用于发布项目的新版本。
