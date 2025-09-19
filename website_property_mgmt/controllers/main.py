# -*- coding: utf-8 -*-

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class WebsitePropertyController(http.Controller):

    def sitemap_property(env, rule, qs):
        """Generate sitemap entries for properties"""
        if not qs or qs.lower() in '/property':
            yield {'loc': '/properties'}

    @http.route(['/property', '/property/page/<int:page>', '/properties', '/properties/page/<int:page>'],
                type='http', auth="public", website=True, sitemap=sitemap_property, readonly=True)
    def properties(self, page=1, **kwargs):
        """Properties listing page"""

        # Get all published properties
        properties = request.env['property.property'].search([
            ('website_published', '=', True)
        ], order='create_date desc')

        website = request.website
        step = 12  # Number of properties per page

        # Pagination
        pager = website.pager(
            url="/property",
            total=len(properties),
            page=page,
            step=step,
            scope=5
        )

        # Get properties for current page
        property_ids = properties[(page - 1) * step:page * step]

        values = {
            'property_ids': property_ids,
            'pager': pager,
            'website': website
        }

        return request.render("website_property_mgmt.index", values)

    @http.route(['/property/<model("property.property"):property>'], type='http', auth="public", website=True, sitemap=True)
    def property_detail(self, property, **post):
        """Single property detail page"""

        values = {
            'property': property.sudo(),
            'main_object': property,
            'website': request.website
        }

        return request.render("website_property_mgmt.property_details", values)

    @http.route(['/property/<model("property.property"):property>/contact'], type='http', auth="user", website=True, sitemap=True)
    def property_contact(self, property, **post):
        values = {
            'property': property.sudo(),
            'main_object': property,
            'website': request.website
        }

        return request.render("website_property_mgmt.property_contact", values)