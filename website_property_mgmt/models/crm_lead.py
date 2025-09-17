from odoo import models, fields


class CRMLead(models.Model):
    _inherit = "crm.lead"

    property_id = fields.Many2one("property.property", string="Property")