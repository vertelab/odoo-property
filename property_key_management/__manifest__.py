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

{
    'name': 'Property: Key Management',
    'version': '18.0.0.0.1',
    # Version ledger: 18.0 = Odoo version. 1 = Major. Non regressionable code.
    # 0 = Minor. 1 = Bug fixes
    'summary': 'Keys and key positions (tubes, shafts, safes) for properties.',
    'category': 'Property',
    'description': '''
Property: Key Management
========================

    Keys belong to the property, not to the asset they open.

    A key tube in the stairwell serves several elevators on the same
    address. Modelling the key as a child of the elevator would duplicate
    it once per elevator and lose the fact that one tube is one physical
    object with one owner.

    This module therefore models the key chain in two levels:

        property.key.position   the physical place the key lives
                                (key tube, shaft, safe, other)
        property.key            the individual key, which opens one or
                                more maintenance assets

    Features:

        - Key positions with address, coordinates and owner
        - Keys with a unique code and a many2many to maintenance assets
        - Archive support on both levels
        - Portal read access to key positions
    ''',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-property/property_key_management',
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel Sverige AB',
    'repository': 'https://github.com/vertelab/odoo-property',
    'depends': [
        'property_mgmt',
        'property_maintanance',
        'maintenance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/property_key_data.xml',
        'views/property_key_position_views.xml',
        'views/property_key_views.xml',
    ],
    'application': False,
    'installable': True,
}
