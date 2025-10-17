from odoo import models, fields, api, _


class ESRSLine(models.Model):
    _inherit = "esrs.line"

    property_id = fields.Many2one("property.property", string="Property", readonly=True, store=True)
