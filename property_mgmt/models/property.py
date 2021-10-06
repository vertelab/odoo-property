from odoo import models, fields, api, _


class PropertyStakeHolder(models.Model):
    _name = 'property.stakeholder'
    _description = "Property Stakeholder"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    partner_status = fields.Selection([('legal_owner', 'Legal Owner'),
                                       ('approving_owner', 'Approving Owner'),
                                       ('former_owner', 'Former Owner'),
                                       ('agent', 'Agent'),
                                       ], string="Status", default='legal_owner')


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
