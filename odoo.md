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