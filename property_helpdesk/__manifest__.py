# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
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
    'name': 'Property Helpdesk',
    'version': '18.0.1.0.0',
    'summary': 'This module is used to maintain properties helpdesk tickets.',
    'category': 'Property',
    'description': '''
Property Helpdesk
=================

    This module is used to maintain properties helpdesk tickets.

    Features:

        - UI Integration: Extends 2 view(s) in the Odoo interface.
        - Extends Odoo: Builds on helpdesk.ticket, property.property.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-property/property_helpdesk',
    'images': ['static/description/banner.png'],  # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-property',
    'depends': ['property_mgmt', 'helpdesk_mgmt'],
    'data': [
        'views/property_view.xml',
        'views/helpdesk_view.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
