from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"
    helpdesk_ticket_id = fields.Many2one("helpdesk.ticket", string="Helpdesk Ticket")
