from odoo import models, fields, api, _
import math


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    # ~ maintenance_equipment_id = fields.Many2one("maintenance.equipment", string="Maintenance Equipment")

    def action_view_maintenance_request(self):
        # ~ kanban_view_id = self.env.ref('maintenance.hr_equipment_view_kanban').id
        # ~ list_view_id = self.env.ref('maintenance.hr_equipment_view_tree').id
        return {
            'name': _("Maintenance Requests"),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,list,form,pivot,graph,calendar,activity',
            # ~ 'views': [(kanban_view_id, 'kanban'), (list_view_id, 'list'), (False, 'form')],
            'domain': [('equipment_id.property_id', '=', self.id)],
            # ~ 'context': {
                # ~ 'default_property_id': self.id
            # ~ }
        }
        
    def action_view_maintenance_equipment(self):
        # ~ kanban_view_id = self.env.ref('maintenance.hr_equipment_view_kanban').id
        # ~ list_view_id = self.env.ref('maintenance.hr_equipment_view_tree').id
        return {
            'name': _("Maintenance Equipment"),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'view_mode': 'kanban,list,form',
            # ~ 'views': [(kanban_view_id, 'kanban'), (list_view_id, 'list'), (False, 'form')],
            'domain': [('property_id', '=', self.id)],
            # ~ 'context': {
                # ~ 'default_property_id': self.id
            # ~ }
        }
        
