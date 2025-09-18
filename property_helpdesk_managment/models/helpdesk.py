from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    maintenance_request_id = fields.Many2one("maintenance.request", string="Maintenance Request")
    maintenance_equipment_id = fields.Many2one("maintenance.equipment", string="Maintenance Equipment")
    maintenance_team_id = fields.Many2one("maintenance.team", string="Maintenance Team")
    
    @api.onchange("property_id")
    def set_equipment_team(self):
        for record in self:
            maintenance_equipment = self.env['maintenance.equipment'].search([('property_id','=',record.property_id.id)], limit=1)
            maintenance_team = self.env['maintenance.equipment'].search([('property_id','=',record.property_id.id)], limit=1).maintenance_team_id
            record.maintenance_equipment_id = maintenance_equipment
            record.maintenance_team_id = maintenance_team_id
        
    def create_maintenance_request(self):
        for record in self:
            if not record.maintenance_request_id:
                if not record.maintenance_equipment_id:
                    raise UserError(_("Please set an equipment before escalating to a maintenance request"))
                    
                if not record.maintenance_team_id:
                    raise UserError(_("Please set a maintenance team before escalating to a maintenance request"))
                
                record.maintenance_request_id = self.env["maintenance.request"].create({
                    'name': record.name,
                    'maintenance_team_id': record.maintenance_team_id.id,
                    'equipment_id': record.maintenance_equipment_id.id,
                    'helpdesk_ticket_id':record.id,
                })
        
