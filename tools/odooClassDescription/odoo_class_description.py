import re
import json
import os

module_name_pattern = r"_name=[\'\"]([\w\.]*?)[\'\"]"
description_pattern = r"_description=u*[\'\"](.*?)[\'\"]"

variable_type_pattern = r'(\w*?)=fields\.(\w*?)\('
variable_string_pattern = r'string=u*[\'\"](.*?)[\'\"]'
brackets_pattern = r'\((.*?)\)'


def run(py_root, out_root):
    print('---------- go! go! go! -------------')
    file_name_list = os.listdir(py_root)

    for file_name in file_name_list:
        if file_name.endswith('.py') and file_name != '__init__.py':
            py_path = os.path.join(py_root, file_name)
            csv_path = os.path.join(out_root, file_name.replace('.py', '.csv'))

            create_csv_from_py(csv_path, py_path)

    print('---------- just so -------------')


def create_csv_from_py(csv_path, py_path):
    info_dict = parse_py(py_path)
    write_to_file(csv_path, info_dict)

def parse_py(file_path):
    info_dict = {}
    current_model = ''
    current_description = ''
    current_variable_info = []

    with open(file_path, 'r') as fp:
        rows = fp.readlines()

    for row in rows:
        row = row.replace(' ', '').replace('\r', '').replace('\n', '')

        result = re.search(module_name_pattern, row)
        if result:
            if current_model:
                info_dict[current_model] = {
                    'description': current_description if current_description else current_model,
                    'variables': current_variable_info
                }

            current_model = result.group(1)
            current_description = ''
            current_variable_info = []

            continue

        result = re.search(description_pattern, row)
        if result:
            if current_model:
                current_description = result.group(1)
            continue                

        result = re.search(variable_type_pattern, row)
        if result:
            if current_model:
                variable_name = result.group(1)
                variable_type = result.group(2)
                variable_info = get_variable_attrs(row, variable_type)
                variable_info['variable_name'] = variable_name
                variable_info['variable_type'] = variable_type
                current_variable_info.append(variable_info)

    if current_model:
        info_dict[current_model] = {
            'description': current_description if current_description else current_model,
            'variables': current_variable_info
        }

    return info_dict


def get_variable_attrs(row, vtype):
    res = {}
    if vtype == 'Selection':
        return res
    elif vtype == 'One2many' or vtype == 'Many2one':
        result = re.search(brackets_pattern, row)
        string_result = re.search(variable_string_pattern, row)
        assert result, row
        assert string_result, row
        emp_raw_string = result.group(1).replace("'", '').replace('"', '').split(',')
        res =  {
            'related': emp_raw_string[0],
            'string': string_result.group(1)
        }
    else:
        result = re.search(variable_string_pattern, row)
        assert result, row

        variable_string = result.group(1)
        res = {'string': variable_string}
    
    return res


def write_to_file(file_path, info_dict):
    with open(file_path, 'w') as fp:
        text = ''

        sorted_key = sorted(info_dict.keys())

        for key in sorted_key:
            value = info_dict[key]
            emp_text = '{}({})\r显示名称,字段,类型,允许空值,关联表,界面显示,说明\rID,ID,Interger,否,,\r'.format(value['description'], key)

            for info in value['variables']:
                var_string = info.get('string', '')
                var_name =  info.get('variable_name', '')
                var_type = info.get('variable_type', '')
                var_related = info.get('related', '')

                emp_text += '{},{},{},,{},,,\r'.format(var_string, var_name, var_type, var_related)
            emp_text += '''创建者,create_uid,Many2one,否,res.users,,
创建时间,create_date,Datetime,否,,,
修改者,write_uid,Many2one,否,res.users,,
修改时间,write_date,Datetime,否,,,
'''
            text += emp_text + '\r\r\r'

        fp.write(text)

if __name__ == "__main__":
    # test_file_path = '/Users/benjilee/Desktop/go_to_trash/test_file/factory_model.py'
    # test_out_path = '/Users/benjilee/Desktop/go_to_trash/test_file/test.csv'

    csv_root = '/Users/benjilee/Desktop/go_to_trash/csv_out'
    py_root = '/Users/benjilee/bplead/work/thingx-chengdu-erp/addons/bp_cl_base/models'

    run(py_root, csv_root)

    py_root = '/Users/benjilee/bplead/work/thingx-chengdu-erp/addons/bp_cl_imd/models'
    run(py_root, csv_root)
        





