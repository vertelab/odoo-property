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
    'version': '18.0.0.0.0',
    'summary': 'This module is used to show properties on the website.',
    'category': 'Property',
    'description': """
        This module is used to show properties on the website.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-property/property_mgmt',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-property',
    'depends': ['website', 'contacts','crm','property_building'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/crm_lead_view.xml',
        'views/property_empty_properties_svg.xml',
        'views/property_property_views.xml',
        'views/property_details_template.xml',
        'views/property_contact_template.xml',
        'views/portal_leads_templates.xml',
        'data/ir_model_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_property_mgmt/static/src/scss/template_common.scss',
            'website_property_mgmt/static/src/scss/template_list.scss',
            'website_property_mgmt/static/src/scss/template_page.scss',
        ],
    },
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
