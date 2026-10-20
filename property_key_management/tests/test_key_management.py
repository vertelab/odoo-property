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

from psycopg2 import IntegrityError

from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class TestKeyManagement(TransactionCase):
    """The key chain is two levels: position (where keys live) and key.

    The important property is that a key belongs to the property, not to the
    asset it opens — one key tube serves several elevators at the same address.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Fastighetsägare AB'})
        cls.equipment_a = cls.env['maintenance.equipment'].create({
            'name': 'Elevator A', 'is_elevator': True,
        })
        cls.equipment_b = cls.env['maintenance.equipment'].create({
            'name': 'Elevator B', 'is_elevator': True,
        })
        cls.position = cls.env['property.key.position'].create({
            'position_type': 'key_tube',
            'street': 'Storgatan 1',
            'zip': '111 22',
            'city': 'Stockholm',
            'owner_id': cls.partner.id,
        })

    def test_position_gets_sequence_name(self):
        self.assertTrue(self.position.name)
        self.assertNotEqual(self.position.name, 'New')

    def test_key_defaults_owner_from_position(self):
        key = self.env['property.key'].create({
            'position_id': self.position.id,
            'code': 'K-001',
        })
        key._onchange_position_id()
        self.assertEqual(key.owner_id, self.partner)

    def test_key_code_must_be_unique(self):
        Key = self.env['property.key']
        Key.create({'position_id': self.position.id, 'code': 'K-DUP'})
        with mute_logger('odoo.sql_db'), self.assertRaises(IntegrityError):
            Key.create({'position_id': self.position.id, 'code': 'K-DUP'})

    def test_one_key_opens_several_assets(self):
        """The many2many is the whole point: one key, several elevators."""
        key = self.env['property.key'].create({
            'position_id': self.position.id,
            'code': 'K-MULTI',
            'equipment_ids': [(6, 0, (self.equipment_a | self.equipment_b).ids)],
        })
        self.assertEqual(key.equipment_count, 2)
        self.assertIn(self.equipment_a, key.equipment_ids)
        self.assertIn(self.equipment_b, key.equipment_ids)

    def test_position_key_count(self):
        self.env['property.key'].create({'position_id': self.position.id, 'code': 'K-A'})
        self.env['property.key'].create({'position_id': self.position.id, 'code': 'K-B'})
        self.position.invalidate_recordset(['key_count'])
        self.assertEqual(self.position.key_count, 2)

    def test_key_action_opens_only_its_assets(self):
        key = self.env['property.key'].create({
            'position_id': self.position.id,
            'code': 'K-ACTION',
            'equipment_ids': [(6, 0, self.equipment_a.ids)],
        })
        action = key.action_view_equipment()
        self.assertEqual(action['res_model'], 'maintenance.equipment')
        self.assertEqual(action['domain'], [('id', 'in', self.equipment_a.ids)])

    def test_archive_hides_key(self):
        key = self.env['property.key'].create({
            'position_id': self.position.id, 'code': 'K-ARCH',
        })
        key.action_archive() if hasattr(key, 'action_archive') else key.write({'active': False})
        self.assertFalse(self.env['property.key'].search([('code', '=', 'K-ARCH')]))
        self.assertTrue(
            self.env['property.key'].with_context(active_test=False)
            .search([('code', '=', 'K-ARCH')])
        )
