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
    'name': 'Property: External Map',
    'version': '16.0.0.0.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'This module adds small and neat features related with the map.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'description': """
    This module adds: \n
      - a map smart button that shows when the city of a property is known.\n
      - a map smart button that redirects user to google map based on the city or latitude and longitude.\n
      - a button to get the latitude and longitude of the property's address .\n
	  This module is maintained from: https://github.com/vertelab/odoo-property
		\n
	  v14.0.1.1.0 Added translation.\n
	  v14.0.1.2.0 Added link to repo in manifest.\n
	  v14.0.1.3.0 Added more Geo-references.\n
	  v14.0.1.3.1 Fixed some labels and debug-mode.\n		  
	  v14.0.1.3.2 changed l10n to i18n.\n	
		  v14.0.1.3.3 added INGEBORG coordinate button and other improvements \n
		  v14.0.1.3.4 added depencency to partner_external_map \n
      v16.0.0.0.0 Ported to 16 and removed dependency to rest_inge.\n
   """,
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-property/property_external_map',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-property',
    # Any module necessary for this one to work correctly

    'depends': ['partner_external_map', 'property_mgmt', 'base_geolocalize'],
    'data': [
        'views/property_view.xml',
        # ~ 'data/data.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
