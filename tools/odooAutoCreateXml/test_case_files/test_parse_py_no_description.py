from odoo import models, fields, api

class ProductionLine(models.Model):
    _name = 'base.production.line'

    code = fields.Char(string='产线编码')
    name = fields.Char(string='产线名称')
    active = fields.Boolean(string='是否启用', defualt=True)
    center = fields.Many2one('base.working.center', string='工作中心')
    table_type = fields.Selection(
        [('fully_auto', '全自动'), ('half_auto', '半自动')],
        string='台帐性质'
    )
    production_lines = fields.One2many('base.production.line', 'center', string='产线')

