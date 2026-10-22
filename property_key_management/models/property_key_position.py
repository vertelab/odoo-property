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
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        ondelete='restrict',
        help='Used when looking up coordinates.',
    )
    latitude = fields.Float(string='Latitude', digits=(16, 8))
    longitude = fields.Float(string='Longitude', digits=(16, 8))
    date_localization = fields.Date(
        string='Geolocation Date',
        readonly=True,
        help='When the coordinates were last looked up.',
    )
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
    equipment_ids = fields.Many2many(
        'maintenance.equipment',
        string='Assets Served',
        compute='_compute_equipment_ids',
        store=True,
        readonly=True,
        help='Every asset opened by any key on this position. A key tube '
             'in the stairwell serves several elevators; this is the '
             'aggregate, so the position can be searched by asset.',
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

    @api.depends('key_ids', 'key_ids.equipment_ids')
    def _compute_equipment_ids(self):
        for position in self:
            position.equipment_ids = position.key_ids.mapped('equipment_ids')

    # ── Geolocation ────────────────────────────────────────────────────
    # A key position is a physical place; the coordinates are what makes
    # it findable on a map when a technician has to go there. Looked up
    # on demand, never on every write: the geocoder is an external call
    # and a bulk import would hammer it.

    def _geo_localize(self, street='', zip_code='', city='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(
            street=street, zip=zip_code, city=city, country=country
        )
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            # Fall back to city only: a street name that the geocoder does
            # not know still gives a useful map position.
            search = geo_obj.geo_query_address(city=city, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def action_geo_localize(self):
        """Look up coordinates for the selected positions.

        Reports the ones that could not be found rather than failing the
        whole batch: one unknown street should not stop the other twenty.
        """
        not_located = self.browse()
        for position in self:
            if not position.street and not position.city:
                continue
            result = position._geo_localize(
                street=position.street,
                zip_code=position.zip,
                city=position.city,
                country=position.country_id.name or 'Sweden',
            )
            if result:
                position.write({
                    'latitude': result[0],
                    'longitude': result[1],
                    'date_localization': fields.Date.context_today(position),
                })
            else:
                not_located |= position

        if not_located:
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 'simple_notification', {
                    'type': 'danger',
                    'title': _('Warning'),
                    'message': _(
                        'Could not find coordinates for: %s',
                        ', '.join(not_located.mapped('name')),
                    ),
                }
            )
        return True
