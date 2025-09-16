from odoo import models, fields, api, _


class PropertyProperty(models.Model):
    _inherit = "property.property"

    esrs_line_ids = fields.One2many('esrs.line', 'property_id', "ESRS Lines")

    @api.depends('esrs_line_ids')
    def _compute_esrs_line(self):
        for rec in self:
            rec.esrs_line_count = len(rec.esrs_line_ids)

    esrs_line_count = fields.Integer(string="ESRS Lines", compute=_compute_esrs_line)

    def action_view_esrs_line(self):
        list_view_id = self.env.ref('csrd_esrs_line.view_esrs_line_list').id
        return {
            'name': _("Property ESRS Lines"),
            'type': 'ir.actions.act_window',
            'res_model': 'esrs.line',
            'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (False, 'form')],
            'domain': [('property_id', '=', self.id)],
            'context': {
                'default_property_id': self.id
            }
        }