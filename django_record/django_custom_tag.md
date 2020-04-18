# django custom tag

## tag common functon

- tag可以获取模版上下文

    ```py
    @register.simple_tag(takes_context=True)
    def current_time(context, format_string):
        timezone = context['timezone']
        return your_get_current_time_method(timezone, format_string)
    ```

- tag接受任意数量的形参，支持直接传参和键值对传参，通过空格分隔

    `{% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}`

## simple tag

simple tag 用于对传入的参数进行简单的处理后返回结果。当在模版中调用时，使用`as`赋给模版变量，在模版中重复使用。例如 `{% current_time "%Y-%m-%d %I:%M %p" as the_time %}`

## inclusion tag

inclusion tag 用于渲染额外的模版。

## advance custom template tags

### django模版简介

模版的工作分为两部分，编译与渲染。自定义tag是需要指明如何编译与渲染。

解析模版内容的方法包含两个形参，parser和token。

parser是一个模版解析器。token包含从模版中读取的原始字符串。

使用token.split_contents()将token分解，获取模版中有用的字符串。

最后将字符串传入自己实现的`template.Node`子类中，对其进行渲染。

关于实现`template.Node`的派生类。其中`render`方法决定渲染的内容。

最后注册tag。tag包含两个参数，name为模版标签的名字，另一个为一个方法对象。如果都不设置，则直接使用方法名作为模版标签的名称。

```py
@register.tag(name="current_time")
def do_current_time(parser, token):
    ...

@register.tag
def shout(parser, token):
    ...
```

## 参考

- https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/#simple-tags
