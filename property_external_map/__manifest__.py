# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Property External Map',
    'version': '14.0.0.1.0',
    'category': 'sale',
    'description': """
        This module adds: \n
          - a map smart button that shows when the city of a property is known.\n
          - a map smart button that redirects user to google map based on the city or latitude and longitude.\n
          - a button to get the latitude and longitude of the property's address .\n
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'https://www.vertel.se',
    'depends': ['base', 'property_mgmt', 'base_geolocalize', 'partner_external_map'],
    'data': [
        'views/property_view.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
