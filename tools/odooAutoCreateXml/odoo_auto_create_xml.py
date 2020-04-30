import os
import re

class AutoOdooXml:

    def __init__(self, path, module_name=None):
        self.root_path = path
        self.model_path = os.path.join(path, 'models')
        self.view_path = os.path.join(path, 'views')
        self.authority_path = os.path.join(path, 'security', 'ir.model.access.csv')

        if not module_name:
            _, module_name = os.path.split(path)

        self.module_name = module_name

        # parse py
        self.current_model = ''
        self.current_attr_list = []
        self.current_one2many_list = []
        self.current_description = ''

        # view
        self.current_view_model = None
        self.current_view_description = None
        self.current_view_attrs = []
        self.current_view_one2many_attrs = []

        self.menuitems = []

    def check_path_exists(self):
        if not os.path.exists(self.root_path):
            print("can't find modules path!")
            return False

        if not os.path.exists(self.view_path):
            os.makedirs(self.view_path)

        dir_authority_path = os.path.dirname(self.authority_path)
        if not os.path.exists(dir_authority_path):
            os.makedirs(dir_authority_path)
        return True

    def run(self):
        print('运行检测....')
        all_is_ok = self.check_path_exists()
        if not all_is_ok:
            return
        print('检查结束！')

        self.create_view_xml()
        print('创建视图文件完成')

        self.write_menu_to_disk()
        print('创建导航栏文件完成')

        self.update_security()
        print('更型权限文件')

        self.get_all_view_name()


    def create_view_xml(self):
        file_name_list = os.listdir(self.model_path)

        for file_name in file_name_list:
            if file_name.endswith('.py') and file_name != '__init__.py' and file_name != '__manifest__.py':
                py_path = os.path.join(self.model_path, file_name)
                self.parse_py_and_write_xml(py_path)

    def parse_py_and_write_xml(self, py_path):
        info_dict = self.parse_py(py_path)
        self.write_view(info_dict)

    def parse_py(self, py_path):
        file_info_dict = {}
        with open(py_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.replace(' ', '').replace('\r', '').replace('\n', '')
            if not line:
                continue

            module_search_result = re.search(r"_name=[\'\"]([\w\.]*?)[\'\"]", line)
            if module_search_result:
                file_info_dict = self.package_current_info(file_info_dict)
                self.current_model = module_search_result.group(1)
                continue

            description_search_result = re.search(r"_description=[\'\"](.*?)[\'\"]", line)
            if description_search_result:
                self.current_description = description_search_result.group(1)
                continue

            one2many_attr_search_result = re.search(r"([\w]*?)=fields.One2many", line)
            if one2many_attr_search_result and self.current_model:
                self.current_one2many_list.append(one2many_attr_search_result.group(1))
                continue

            attr_search_result = re.search(r"([\w]*?)=fields", line)
            if attr_search_result and self.current_model:
                self.current_attr_list.append(attr_search_result.group(1))
        
        return self.package_current_info(file_info_dict)

    def package_current_info(self, file_info_dict):
        if self.check_is_time_package_info():
            if not self.current_description:
                self.current_description = self.current_model.replace('.', '_')
            file_info_dict[self.current_model] = {
                'attrs': self.current_attr_list,
                'one2many_attrs': self.current_one2many_list,
                'description': self.current_description
            }
            self.menuitems.append((self.current_model, self.current_description))
            self.current_model = ''
            self.current_attr_list = []
            self.current_one2many_list = []
            self.current_description = ''
        return file_info_dict
        
    def check_is_time_package_info(self):
        return self.current_model and (len(self.current_attr_list) != 0 or len(self.current_one2many_list) != 0)

    def write_view(self, file_info_dict):
        for model, value in file_info_dict.items():
            self.current_view_model = model
            self.current_view_description = value['description']
            self.current_view_attrs = value['attrs']
            self.current_view_one2many_attrs = value['one2many_attrs']


            xml_file_name = model.replace('.', '_') + '_view.xml'
            xml_file_path = os.path.join(self.view_path, xml_file_name)
            if not os.path.exists(xml_file_path):
                with open(xml_file_path, 'w') as file:
                    xml = self.create_view_string()
                    file.write(xml)

    def create_view_string(self):
        xml_template = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
{content}
    </data>
</odoo>
        '''

        form_view = self.create_form_view()
        tree_view = self.create_tree_view()
        action_view = self.create_action_view()

        return xml_template.format(content=form_view + tree_view + action_view)

    def create_form_view(self):
        id = self.current_view_model.replace('.', '_') + '_form_view'

        form_xml_template = '''
        <record id="{id}" model="ir.ui.view">
            <field name="name">{name}</field>
            <field name="model">{module_name}</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
{form}
                        </group>
{page}
                    </sheet>
                </form>
            </field>
        </record>
        '''

        form_content = ''
        for attr in self.current_view_attrs:
            form_content += ' ' * 28 + '<field name="{}"/>\r'.format(attr)

        page_content = ''
        if self.current_view_one2many_attrs:
            page_formate = ' ' * 28 + '<page string="PageName">\r' + '{}' + ' ' * 28 + '</page>\r'
            for attr in self.current_view_one2many_attrs:
                emp_page_content = ' ' * 32 + '<field name="{}"/>\r'.format(attr)
                page_content += page_formate.format(emp_page_content)
            page_content = ' ' * 24 + '<notebook>\r' + page_content + ' ' * 24 + '</notebook>'

        return form_xml_template.format(
            id=id, name=id, module_name=self.current_view_model, form=form_content,
            page=page_content
        )

    def create_tree_view(self):
        id = self.current_view_model.replace('.', '_') + '_tree_view'

        tree_xml_template = '''
        <record id="{id}" model="ir.ui.view">
            <field name="name">{name}</field>
            <field name="model">{module_name}</field>
            <field name="arch" type="xml">
                <tree>
{form}
                </tree>
            </field>
        </record>
        '''

        form_content = ''
        for attr in self.current_view_attrs:
            form_content += ' ' * 20 + '<field name="{}"/>\r'.format(attr)

        return tree_xml_template.format(id=id, name=id, module_name=self.current_view_model, form=form_content)

    def create_action_view(self):
        origin_id = self.current_view_model.replace('.', '_')
        action_view = '''
        <record id="{origin_id}_action" model="ir.actions.act_window">
            <field name="name">{name}</field>
            <field name="res_model">{model}</field>
            <field name="type">ir.actions.act_window</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="domain">[]</field>
        </record>
        <record id="{origin_id}_form_action" model="ir.actions.act_window.view">
            <field name="view_mode">form</field>
            <field name="view_id" ref="{origin_id}_form_view"/>
            <field name="sequence">2</field>
            <field name="act_window_id" ref="{origin_id}_action"/>
        </record>
        <record id="{origin_id}_tree_action" model="ir.actions.act_window.view">
            <field name="view_mode">tree</field>
            <field name="view_id" ref="{origin_id}_tree_view"/>
            <field name="sequence">1</field>
            <field name="act_window_id" ref="{origin_id}_action"/>
        </record>
        '''.format(origin_id=origin_id, name=self.current_view_description, model=self.current_view_model)
        return action_view

    def write_menu_to_disk(self):
        menu_path = os.path.join(self.view_path, 'menu.xml')
        if not os.path.exists(menu_path):
            with open(menu_path, 'w') as file:
                menu_xml = self.create_menu_string()
                file.write(menu_xml)

    def create_menu_string(self):
        menu_template = '''<?xml version="1.0" encoding="UTF-8" ?>
<odoo>
    <menuitem name="{module_name}" id="{module_name}_menu_root"/>
{menuitems}
</odoo>
        '''
        menuitems_string = ''
        menuitem_template = '''
        <menuitem name="{description}" id="{id}_menu" action="{id}_action"
                      parent="{module_name}_menu_root"/>
        '''
        for key, description in self.menuitems:
            menuitems_string += menuitem_template.format(
                description=description,
                id=key.replace('.', '_'),
                module_name=self.module_name,
            )

        return menu_template.format(module_name=self.module_name, menuitems=menuitems_string)

    def update_security(self):
        need_security_models = self.get_need_security_model()

        security_string = ''
        for model in need_security_models:
            id = 'access_' + model
            security_string += '{id},{id},{model},base.group_user,1,1,1,1\r'.format(id=id, model=model)

        if security_string:
            with open(self.authority_path, 'a') as file:
                file.write('\r' + security_string)


    def get_need_security_model(self):
        need_security_modes = []

        exist_security_model = self.parse_security()

        for model, _ in self.menuitems:
            model_name = 'model_{}'.format(model.replace('.', '_'))

            if model_name not in exist_security_model:
                need_security_modes.append(model_name)

        return need_security_modes

    def parse_security(self):
        with open(self.authority_path, 'r') as file:
            lines = file.readlines()

        models_names = []
        if len(lines) <= 1:
            return []

        for line in lines[1:]:
            line_splite_list = line.replace('\r', '').replace('\n', '').split(',')

            if len(line_splite_list) == 8:
                models_names.append((line_splite_list[2]))

        return models_names


    def get_all_view_name(self):
        name_list = os.listdir(self.view_path)

        for name in name_list:
            if name != 'menu.xml':
                print("'views/{}',".format(name))
        print("'views/menu.xml',")


if __name__ == "__main__":
    path = '/Users/benjilee/bplead/work/thingx-chengdu-erp/addons/test_model'
    test_obj = AutoOdooXml(path, '功能测试')
    test_obj.run()