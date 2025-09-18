from odoo import models, fields, api, _

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    property_id = fields.Many2one("property.property", string="Property")



