# odoo10

## 权限

odoo中的权限控制分为三种：对模型的权限、对记录的权限、对字段的权限。

实现权限控制的前提是设置用户组。

对模型权限：定义在ir.model.acess.csv文件中，主要控制用户组对于模型的读、写、创建、删除。

__对记录权限__ ：通过xml定义，定义用户组用户对于数据库中记录的读、写、创建、删除。

对于记录的权限常见用法：限制用户只可访问与自己有关的记录。

```xml
<record id="delete_cancelled_only" model="ir.rule">
        <field name="name">Only cancelled leads may be deleted</field>
        <field name="model_id" ref="crm.model_crm_lead"/>
        <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
        <field name="perm_read" eval="0"/>
        <field name="perm_write" eval="0"/>
        <field name="perm_create" eval="0"/>
        <field name="perm_unlink" eval="1" />
        <field name="domain_force">[('state','=','cancel')]</field>
    </record>
```

对字段的权限：通过field中增加group定义用户对于字段、按钮的可视权限。

## filed compute

记录关于field的compute与store参数的用法。

field上增加compute后，在数据库中不存储该列。只是在页面显示时会调用compute关联的方法计算值。因此，在前端页面上无法用该属性进行排序。

compute和store=True同时使用时，若该字段在数据库中不存在，则会将由compute函数计算的值存储在数据库中；若该值已存在，则跳过compute方法，直接从数据库中取值。

## odoo10中使用ir.values实现视图动作绑定

思路：通过ir.values创建一个动作，该动作指向一个action，通过该action完成一些数据操作。

代码实现:
[参考](https://www.cnblogs.com/joshuajan/p/6258028.html
)
```xml
# server action
<record model="ir.actions.server" id="order_confirm_func">
    <field name="name">order confirm</field>
    <field name="model_id" ref="model_bp_stock_order"/>
    <field name="code">
        raise Warning('warning message!')
        <!--model.browse(env.context.get('active_ids')).confirm()-->
    </field>
</record>

# 动作功能测试
<record model="ir.values" id="order_confirm_action">
    <field name="model_id" ref="model_bp_stock_order"/>
    <field name="name">订单批次确认</field>
    <field name="key2">client_action_multi</field>
    <field name="value" eval="'ir.actions.server,'+str(ref('order_confirm_func'))"/>
    <field name="key">action</field>
    <field name="model">bp.stock.order</field>
</record>
```

该方法在odoo10中可行，但在odoo12中是否可行还未研究。


## odoo通过弹窗返回信息

odoo中的视图都依赖于一个model，是否存在一冲视图不依赖于model，只是展示过程信息，这些信息都不需要存储在数据库汇总。
> 简便的方法是通过 ```raise UserError(msg)```。应该还可以通过自定义一个form视图，实现这个功能。

## 如何控制odoo的前端css布局？

TODO

## postgresql主键自增

与mysql不同，postgresql通过serial和bigserial实现。

serial 和 bigserial 类型不是真正的类型，只是为在表中设置唯一标识做的概念上的便利。不过是一种便捷的封装。

通过serial和bigserial只是实现了字段的自增，还要添加primary key实现主键约束。

----

## postgrel char(n)、varchar(n)、text之间的比较

postgresql中char(n)、varchar(n)、text之间当字符串相等时，这三种类型可以直接相互比较。

postgresql中显式类型转换 `cast (v as type)`

## postgresql中查看所有的数据库、某一数据库中的数据表以及某张表的构成?

- __\\?__: 查看所有的相关命令
- __\l__: list all database
- __\dt__: list all table
- __\d tableName__ : descrip a table

----

## odoo12 client_action绑定自定义js文件？

[产考链接](https://segmentfault.com/a/1190000017087118)

不过在我实验的时候还是遇到了奇怪的问题。我打开页面js一直报错————无法找到我定义的client_action的tag，这个问题我找了很久，一直无法定位问题点。后来尝试性的将menuitem和client_action放在同一个xml文件下，问题就解决了。当时出问题的原因仍未确定。

----

odoo12中菜单不显示的问题？

odoo12与odoo10创建新模块后的默认权限不同。odoo10中是默认有所有权限，而odoo12中需要在csv中定义权限。

----

postgresql中对于now()设置时区
```sql
now() AT TIME ZONE 'utc'
```