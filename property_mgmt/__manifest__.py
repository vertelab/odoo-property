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
    'name': 'Property: Mgmt',
    'version': '14.0.1.0.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'This module is used to manage properties and link it to a partner.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'description': """
    This module is used to manage properties and link it to a partner. \n
    User creates a Property and adds stakeholders (res.partner), their role and percentage. \n
    User can also add an agent to the list of stakeholders if the property has an agent. \n
        
    Here is the link to how it works: https://www.loom.com/share/36bf5bd5f7774d68be75243feb7144b9\n
    v14.0.1.2.0 New version number and added translation. \n
        v14.0.1.3.0 Added link to repository: https://github.com/vertelab/odoo-property	\n
        v14.0.1.4.0 - Added field for numerator, denominator and tax unit \n
        v14.0.1.5.0 - Added Server Action to get properties for multiple partners \n
        v14.0.1.6.0 - Added Property user group and property manager group
    """,
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-property/property_mgmt',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-propperty',
    # Any module necessary for this one to work correctly
    
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/property_security.xml',
        'views/menu.xml',
        'views/property_view.xml',
        'views/property_stakeholder_view.xml',
        # 'views/property_designation_view.xml',
        # 'views/property_history_view.xml',
        'views/res_partner_view.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
