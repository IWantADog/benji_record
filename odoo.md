# odoo10

## 权限

odoo中的权限控制分为三种：对模型的权限、对记录的权限、对字段的权限。

实现权限控制的前提是设置用户组。

对模型权限：定义在ir.model.acess.csv文件中，主要控制用户组对于模型的读、写、创建、删除。

__对记录权限__ ：通过xml定义，定义用户组用户对于那些记录具有读、写、创建、删除权限。

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

## odoo12中增加动作

```xml
<record model="ir.actions.server" id="create_table_report">
    <field name="name">批量创建台位报告</field>
    <field name="model_id" ref="model_base_table"/>
    <field name="binding_model_id" ref="model_base_table"/>
    <field name="state">code</field>
    <field name="code">
    <!-- records对应所有选中的records -->
        if records:
            records.create_table_report()
    </field>
</record>
```

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

## 2019.10.22

odoo中controller中设置auth=“public”时需要创建一个开放用户。[参考](https://www.odooyun.com/documentation/reference/http.html#routing)


## 2019.10.23

视图继承详解 odoo12/doc/reference/view.rst

----

从未见过的视图使用方式。

```xml
<field name="move_line_nosuggest_ids" attrs="{'readonly': [('state', 'in', ('done', 'cancel'))]}" context="{'tree_view_ref': 'stock.view_stock_move_line_operation_tree','default_picking_id': picking_id, 'default_move_id': id, 'default_product_id': product_id, 'default_location_id': location_id, 'default_location_dest_id': location_dest_id}"/>
```

### odoo中参数模块设置

res.config.settings
odoo/addons/base/models/res_config.py

### odoo xmlrpc

[链接](https://www.odooyun.com/documentation/webservices/odoo.html)

### odoo image store by base64 string

image binary to base64 string

```python
import base64
from cStringIO import StringIO

# pip2 install pillow
from PIL import Image


def image_to_base64(image_path):
    img = Image.open(image_path)
    output_buffer = StringIO()
    img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return base64_data
```

### only debug can see it

```
groups="base.group_no_one"
```

### qweb渲染模版

```js
var self = this;
var html = $(QWeb.render('equipment_ratio_detail_template', { data:data }));
$('.bp-ratio-detail').html(html);
```

### update join [参考](https://www.postgresql.org/message-id/6ca02fc80806231243y6e4ea774x6ae4967fb8824447@mail.gmail.com)

```sql
update eam_equipment_running_record as a set running_hours_plan=86399
from eam_equipment b
where a.equipment_id=b.id and b.running_id=3 and date between '2019-11-18' and current_date;
```

### Widgets

[详解](https://www.odooyun.com/documentation/reference/javascript_reference.html#widgets)

widget默认会渲染绑定的模版。

通过widget.variable在xml模版中获取js中的变量。

### tag

```xml
<field name="tag">ghcc_work.work_application_menu_tag</field>
```

### action.client

1. action.client定义tag。tag必须包含模块名

2. 声明template。关键点t-name

3. js文件，将widget通过tag注册到action上

4. 将js文件通过xpath插入assets_backend

5. 将xml加入__manifest__中的data，template加入qweb中。

### 当前登录用户的id

- xml中访问当前用户的id `user.id`

- 在domain中获取当前登录用户的id `uid`

- domain中`active_id`当前record的id

- odoo10&&py中当前用户 `self.user.id or self._uid`

- odoo12&&py中通过`self.env.user`获取当前登录用户。

### windows server deploy

- windows中将odoo作为服务启动nssm

- 共享资源中文件出现‘clound find commend lessc’，不是由于less的安装问题，好像是使用nssc启动服务时出现的问题，删除服务重新安装后解决。

- __odoo could find lessc__ 卸载之前装的less，重新全局安装 `cnpm install -g less; cnpm install -g less-plugin-clean-css`

- 切换网站主题时出现lessc could find 问题:在conf文件中增加 __bin_path=/path/to/thirdpartypath/to/thirdparty__

- odoo.conf的参数事例[odoo.conf](https://github.com/odoo/odoo/issues/4141)

- [how-to-create-executable-file-for-odoo-project](https://stackoverflow.com/questions/39566718/how-to-create-executable-file-for-odoo-project)

### odoo视图的加载问题

odoo中__mainfest__ 中data包含的模版加载是有先后顺序的，按照列表的先后次序加载。如果前面的视图文件引用了后面的视图数据，升级模块是会报错。

### odoo12 client action [link](https://www.odooyun.com/documentation/reference/javascript_reference.html#client-actions)

### odoo12与odoo10区别

- `ir.needaction_mixin`在odoo10中使用，odoo12中使用`mail.activity.mixin`

- Registry

    ```python
    # in odoo12
    from odoo.modules.registry import Registry

    # in odoo10
    from odoo.modules.registry import RegistryManager
    ```

### base.user_has_groups 判断当前登录用户是否在指定的权限组中

### odoo ajax post 请求

客户端: data必须包含params
服务器端: type='json'

关于csrf(跨域请求伪造)没搞懂，暂时将csrf设置为False。

ajax发送跨域请求时会首先发送一个option请求。

### odoo批量图片导入

odoo image store by base64 string

image binary to base64 string

```python
import base64
from cStringIO import StringIO

# pip2 install pillow
from PIL import Image


def image_to_base64(image_path):
    img = Image.open(image_path)
    output_buffer = StringIO()
    img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return base64_data
```

### odoo.api.constrains使用

Decorates a constraint checker. Each argument must be a field name used in the check:

@api.one
@api.constrains('name', 'description')
def _check_description(self):
    if self.name == self.description:
        raise ValidationError("Fields name and description must be different")
Invoked on the records on which one of the named fields has been modified.

Should raise ValidationError if the validation failed.

__Warning__
>@constrains only supports simple field names, dotted names (fields of relational fields e.g. partner_id.customer) are not supported and will be ignored

>@constrains will be triggered only if the declared fields in the decorated method are included in the create or write call. It implies that fields not present in a view will not trigger a call during a record creation. A override of create is necessary to make sure a constraint will always be triggered (e.g. to test the absence of value).

### odoo _sql_constraint使用

_sql_constraint = [
    ('constraint_name', 'unique(attrs)', 'message that user should know')
]

注意事项

1. 如果数据中存在与约束冲突的数据，约束无法创建

2. 对于多属性组合唯一约束，_sql_constraint只会在数据创建是检查，无法监控存在的数据的修改

3. 为了完善多属性组合唯一约束，将`_sql_constraint`与`@api.constrains`组合使用

### postgresql常用命令

- __\\?__: 查看所有的相关命令
- __\l__: list all database
- __\dt__: list all table
- __\d tableName__ : descrip a table

### postgresql主键自增。bigserial [链接](https://www.yiibai.com/manual/postgresql/datatype-numeric.html#DATATYPE-SERIAL)

### 隐藏菜单

```xml
<record id="hr.menu_hr_root" model="ir.ui.menu">
        <field name="active" eval="False"/>
</record>
```
