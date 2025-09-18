from odoo import models, fields, api, _
import math


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    # ~ maintenance_equipment_id = fields.Many2one("maintenance.equipment", string="Maintenance Equipment")

    def action_view_helpdesk_ticket(self):
        # ~ kanban_view_id = self.env.ref('maintenance.hr_equipment_view_kanban').id
        # ~ list_view_id = self.env.ref('maintenance.hr_equipment_view_tree').id
        return {
            'name': _("Helpdesk Tickets"),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'kanban,list,form',
            # ~ 'views': [(kanban_view_id, 'kanban'), (list_view_id, 'list'), (False, 'form')],
            'domain': [('property_id', '=', self.id)],
            # ~ 'context': {
                # ~ 'default_property_id': self.id
            # ~ }
        }
        
