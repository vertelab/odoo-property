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


class PropertyKey(models.Model):
    """An individual key.

    A key opens one or more assets (elevators, doors, plant rooms). The
    many2many is deliberate: one key commonly opens several elevators in
    the same shaft, and one elevator is commonly opened by several keys
    (service key, master key, emergency key).
    """

    _name = 'property.key'
    _description = 'Property Key'
    _order = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('property.key') or _('New'),
        tracking=True,
    )
    position_id = fields.Many2one(
        'property.key.position',
        string='Key Position',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True,
    )
    property_id = fields.Many2one(
        'property.property',
        string='Property',
        related='position_id.property_id',
        store=True,
        readonly=True,
        index=True,
    )
    code = fields.Char(
        string='Key Code',
        required=True,
        tracking=True,
        help='Unique code stamped on the key or recorded in the key '
             'register. Must be unique across all keys.',
    )
    key_type = fields.Selection(
        selection=[
            ('service', 'Service Key'),
            ('master', 'Master Key'),
            ('emergency', 'Emergency Key'),
            ('user', 'User Key'),
            ('other', 'Other'),
        ],
        string='Key Type',
        default='service',
        required=True,
        tracking=True,
    )
    equipment_ids = fields.Many2many(
        'maintenance.equipment',
        'property_key_maintenance_equipment_rel',
        'key_id',
        'equipment_id',
        string='Opens Assets',
        help='The assets this key gives access to — elevators, doors, '
             'plant rooms.',
    )
    equipment_count = fields.Integer(
        string='Asset Count',
        compute='_compute_equipment_count',
    )
    owner_id = fields.Many2one(
        'res.partner',
        string='Owner',
        tracking=True,
        help='Who holds this key. Defaults to the key position owner.',
    )
    issued_date = fields.Date(string='Issued On', tracking=True)
    returned_date = fields.Date(string='Returned On', tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        (
            'code_uniq',
            'unique(code)',
            'The key code must be unique.',
        ),
    ]

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for key in self:
            key.equipment_count = len(key.equipment_ids)

    @api.onchange('position_id')
    def _onchange_position_id(self):
        """Default the key owner to the key position owner."""
        if self.position_id and not self.owner_id:
            self.owner_id = self.position_id.owner_id

    def action_view_equipment(self):
        self.ensure_one()
        return {
            'name': _('Assets opened by %s', self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.equipment_ids.ids)],
        }
