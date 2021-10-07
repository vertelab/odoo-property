from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_stakeholder_ids = fields.One2many('property.stakeholder', 'partner_id', string="Properties",
                                               domain=[('property_id.state', '=', 'ok')])
