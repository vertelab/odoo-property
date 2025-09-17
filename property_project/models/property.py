from odoo import models, fields, api, _
import math


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    def action_view_project(self):
        # ~ kanban_view_id = self.env.ref('maintenance.hr_equipment_view_kanban').id
        # ~ list_view_id = self.env.ref('maintenance.hr_equipment_view_tree').id
        return {
            'name': _("Property Projects"),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'kanban,list,form',
            # ~ 'views': [(kanban_view_id, 'kanban'), (list_view_id, 'list'), (False, 'form')],
            'domain': [('property_id', '=', self.id)],
            'context': {
                'default_property_id': self.id
            }
        }
        
    def action_view_project_task(self):
        # ~ kanban_view_id = self.env.ref('maintenance.hr_equipment_view_kanban').id
        # ~ list_view_id = self.env.ref('maintenance.hr_equipment_view_tree').id
        return {
            'name': _("Property Tasks"),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'kanban,list,form,calendar,pivot,graph,activity',
            # ~ 'views': [(kanban_view_id, 'kanban'), (list_view_id, 'list'), (False, 'form')],
            'domain': [('property_id', '=', self.id)],
            'context': {
                'default_property_id': self.id
            }
        }
