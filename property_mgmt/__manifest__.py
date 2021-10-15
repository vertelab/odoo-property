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
    'name': 'Property Management',
    'version': '14.0.1.3.0',
    'category': 'sale',
    'description': """
        This module is used to manage properties and link it to a partner. \n
        User creates a Property and adds stakeholders (res.partner), their role and percentage. \n
        User can also add an agent to the list of stakeholders if the property has an agent. \n
		\n
        Here is the link to how it works: https://www.loom.com/share/36bf5bd5f7774d68be75243feb7144b9
		\n
		v14.0.1.2.0 New version number and added translation.\n
		v14.0.1.3.0 Added link to repository: https://github.com/vertelab/odoo-property
		\n
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'https://www.vertel.se',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
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
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
