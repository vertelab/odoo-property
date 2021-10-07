from odoo import models, fields, api, _


class PropertyProperty(models.Model):
    _name = 'property.property'
    _description = "Property"
    _inherits = {'res.partner': 'partner_id'}

    name = fields.Char(string="Description")
    code = fields.Char(string="Property Code")
    acquired_date = fields.Date(string="Acquired Date")
    size = fields.Char(string="Property Size")
    property_status = fields.Selection([('no_building', 'No Building'), ('has_building', 'Has Building')],
                                       default='has_building')
    state = fields.Selection([('new', 'New'), ('ok', 'OK'), ('archived', 'Archived')], string="State", default='new')

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    longitude = fields.Float(string='Geo Longitude', digits=(16, 5))

    has_agent = fields.Boolean(string="Has Agent")
    agent_name = fields.Char(string="Agent Name")
    agent_phone_number = fields.Char(string="Agent Phone Number")
    stakeholder_ids = fields.One2many('property.stakeholder', 'property_id', string="Stakeholders")

    partner_id = fields.Many2one('res.partner', string="Contact Person", required=True)

    partner_status = fields.Selection([('legal_owner', 'Legal Owner'),
                                       ('approving_owner', 'Approving Owner'),
                                       ('former_owner', 'Former Owner'),
                                       ('agent', 'Agent'),
                                       ], string="Contact's Status", default='legal_owner')

    def approved_property(self):
        self.write({
            'state': 'ok'
        })


class PropertyStakeHolder(models.Model):
    _name = 'property.stakeholder'
    _description = "Property Stakeholder"
    _inherits = {'res.partner': 'partner_id', 'property.property': 'property_id'}

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    partner_status = fields.Selection([('legal_owner', 'Legal Owner'),
                                       ('approving_owner', 'Approving Owner'),
                                       ('former_owner', 'Former Owner'),
                                       ('agent', 'Agent'),
                                       ], string="Status", default='legal_owner')
    percentage = fields.Float(string="Percentage(%)")
    property_id = fields.Many2one('property.property', string="Property")


class PropertyDesignation(models.Model):
    _name = 'property.designation'
    _description = "Property Designation"
    _inherits = {'res.partner': 'partner_id'}

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    state = fields.Selection([('New', 'New'), ('OK', 'OK'), ('Archived', 'Archived')], string="State", default='New')
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = "Property History"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    note = fields.Text(string="Note")
