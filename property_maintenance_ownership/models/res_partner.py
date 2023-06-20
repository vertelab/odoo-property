from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError

class ResPartnerEquipment(models.Model):
    _inherit = 'res.partner'

    equipment_count = fields.Integer(
        string='Equipment',
        compute='_compute_equipment_count',
        readonly=True
    )

    def _compute_equipment_count(self):
        for partner in self:
            partner.equipment_count = self.env['maintenance.equipment'].search_count([
                ('technician_user_id.partner_id', '=', partner.id)
            ])







