from odoo import models, fields, api, _
import math


class PropertyProperty(models.Model):
    _name = 'property.property'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Property"
    
    acquired_date = fields.Date(string="Acquired Date")
    city = fields.Char()
    code = fields.Char(string="Property Code")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    company_id = fields.Many2one(comodel_name='res.company',string='Company',default=lambda self: self.env.company,)
    currency_id = fields.Many2one(related="company_id.currency_id",string="Currency",)
    created_date = fields.Date(string="Created On", default=fields.Date.context_today)
    description = fields.Text(string='Description')
    image_1920 = fields.Image(string="Image", help="Image of the property", max_width=1920, max_height=1920)
    name = fields.Char(string="Description")
    parent_property_id = fields.Many2one('property.property')
    property_status = fields.Selection([('no_building', 'No Building'), ('has_building', 'Has Building')], default='has_building')
    tag_ids = fields.Many2many("property.tag", string="Property Tags", help="Tags for the property")
    size = fields.Char(string="Property Size")
    stakeholder_ids = fields.One2many('property.stakeholder', 'property_id', string="Stakeholders", auto_join=True)
    state = fields.Selection([('new', 'New'), ('ok', 'OK'), ('archived', 'Archived')], string="State", default='new')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',domain="[('country_id', '=?', country_id)]")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    
    def approved_property(self):
        self.write({
            'state': 'ok'
        })


class PropertyStakeHolder(models.Model):
    _name = 'property.stakeholder'
    _description = "Property Stakeholder"
    # _inherits = {'res.partner': 'partner_id', 'property.property': 'property_id'}
    _inherits = {'property.property': 'property_id'}

    partner_id = fields.Many2one('res.partner', string="Partner", required=True, index=True)
    partner_status = fields.Selection([('legal_owner', 'Legal Owner'),
                                       ('approving_owner', 'Approving Owner'),
                                       ('former_owner', 'Former Owner'),
                                       ('agent', 'Agent'),
                                       ('tenant', 'Tenant'),
                                       ('property_manager', 'Property Manager'),
                                       ], string="Status", default='legal_owner')

    property_id = fields.Many2one('property.property', string="Property", index=True, required=True, ondelete='cascade')
    property_state = fields.Selection(string="State",
                                      related='property_id.state')

    stakeholder_tax_unit = fields.Char(string="Tax Unit")
    percentage = fields.Integer(string="Percentage(%)",)


class PropertyDesignation(models.Model):
    _name = 'property.designation'
    _description = "Property Designation"
    # _inherits = {'res.partner': 'partner_id'}

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    state = fields.Selection([('New', 'New'), ('OK', 'OK'), ('Archived', 'Archived')], string="State", default='New')
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, index=True)


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = "Property History"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    note = fields.Text(string="Note")
