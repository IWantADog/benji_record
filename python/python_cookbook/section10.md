# python cookbook section 10

## 运行目录或压缩文件

如果你的应用程序已经有多个文件，你可以把你的应用程序放进它自己的目录并添加一个__main__.py文件。 举个例子，你可以像这样创建目录：

```
myapplication/
    spam.py
    bar.py
    grok.py
    __main__.py
```

如果__main__.py存在，你可以简单地在顶级目录运行Python解释器：
`bash % python3 myapplication`

## 分发包

要让你的包可以发布出去，首先你要编写一个 setup.py ，类似下面这样：

```py
# setup.py
from distutils.core import setup

setup(
    name='projectname',
    version='1.0',
    author='Your Name',
    author_email='you@youraddress.com',
    url='http://www.you.com/projectname',
    packages=['projectname', 'projectname.utils'],
)
```

下一步，就是创建一个`MANIFEST.in`文件，列出所有在你的包中需要包含进来的非源码文件：

```py
# MANIFEST.in
include *.txt
recursive-include examples *
recursive-include Doc *
```

确保`setup.py`和`MANIFEST.in`文件放在你的包的最顶级目录中。一旦你已经做了这些，你就可以像下面这样执行命令来创建一个源码分发包了：

`% bash python3 setup.py sdist`
它会创建一个文件比如”projectname-1.0.zip” 或 “projectname-1.0.tar.gz”, 具体依赖于你的系统平台。如果一切正常， 这个文件就可以发送给别人使用或者上传至`Python Package Index`.
