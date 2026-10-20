# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _


class PropertyKeyPosition(models.Model):
    """The physical place where keys are kept.

    A key tube in the stairwell, a shaft, a safe — one physical object at
    one address. Keys hang on a position; the position belongs to the
    property, not to any single asset it gives access to.
    """

    _name = 'property.key.position'
    _description = 'Key Position'
    _order = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('property.key.position') or _('New'),
        tracking=True,
    )
    property_id = fields.Many2one(
        'property.property',
        string='Property',
        index=True,
        tracking=True,
        help='The property this key position belongs to.',
    )
    position_type = fields.Selection(
        selection=[
            ('key_tube', 'Key Tube'),
            ('shaft', 'Shaft'),
            ('safe', 'Safe'),
            ('other', 'Other'),
        ],
        string='Position Type',
        required=True,
        default='key_tube',
        tracking=True,
    )
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street (line 2)')
    zip = fields.Char(string='ZIP')
    city = fields.Char(string='City')
    latitude = fields.Float(string='Latitude', digits=(16, 8))
    longitude = fields.Float(string='Longitude', digits=(16, 8))
    owner_id = fields.Many2one(
        'res.partner',
        string='Owner',
        tracking=True,
        help='Who holds the key position — usually the property owner '
             'or the facility manager.',
    )
    key_ids = fields.One2many(
        'property.key',
        'position_id',
        string='Keys',
    )
    key_count = fields.Integer(
        string='Key Count',
        compute='_compute_key_count',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('key_ids')
    def _compute_key_count(self):
        for position in self:
            position.key_count = len(position.key_ids)

    @api.onchange('property_id')
    def _onchange_property_id(self):
        """Prefill the address from the property.

        The key position usually sits at the property's address; copying it
        saves typing and keeps the two in sync at creation time.
        """
        if self.property_id and not self.street:
            self.street = self.property_id.street
            self.street2 = self.property_id.street2
            self.zip = self.property_id.zip
            self.city = self.property_id.city

    def action_view_keys(self):
        self.ensure_one()
        return {
            'name': _('Keys — %s', self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'property.key',
            'view_mode': 'list,form',
            'domain': [('position_id', '=', self.id)],
            'context': {'default_position_id': self.id},
        }
