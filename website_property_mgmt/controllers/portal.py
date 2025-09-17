# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class LeadPortal(CustomerPortal):

    @http.route(['/my/leads', '/my/leads/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_leads(self, page=1, sortby='name', **kw):
        """
        Displays the CRM leads tree view filtered by the logged-in user.
        """
        partner_id = request.env.user.partner_id
        user_id = request.env.user
        lead_obj = request.env['crm.lead'].sudo()
        source_ids = request.env['utm.source'].sudo().search([])
        filter_source_id = kw.get('source')
        domain = [('partner_id', '=', partner_id.id), ('property_id', '!=', False)]

        search = kw.get('search', '').strip()
        if search:
            domain += [('name', 'ilike', search)]
        if filter_source_id:
            domain += [('source_id', '=', int(filter_source_id))]

        items_per_page = 10
        total_leads = lead_obj.search_count(domain)

        sorted_list = {
            'name': {'label': 'Name', 'order': 'name asc'},
            'date': {'label': 'Assignation Date', 'order': 'create_date asc'},
        }
        order = sorted_list[sortby]['order']
        pager = portal_pager(
            url="/my/leads",
            total=total_leads,
            page=page,
            url_args={'sortby': sortby},
            step=items_per_page
        )

        leads = lead_obj.search(domain, order=order, limit=items_per_page, offset=pager['offset'])

        has_quotations = bool(request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner_id.id),
            ('opportunity_id', 'in', leads.ids)
        ], limit=1))

        values = {
            'leads': leads,
            'has_quotations': has_quotations,
            'page_name': 'leads',
            'pager': pager,
            'sortby': sortby,
            'searchbar_sortings': sorted_list,
            'partner_id': partner_id,
            'user_id': user_id,
            'source_ids': source_ids,
        }

        return request.render('website_property_mgmt.portal_my_leads', values)

    @http.route(["/my/lead/<model('crm.lead'):lead_id>"], type="http", auth="user", website=True)
    def action_view_lead_details(self, lead_id):
        """
        Displays the read-only form view of a CRM lead.
        """
        partner_id = request.env.user.partner_id
        user_id = request.env.user
        domain = ['|', ('partner_id', '=', partner_id.id), ('user_id', '=', user_id.id)]
        all_leads = request.env['crm.lead'].sudo().search(domain)
        lead_ids = all_leads.ids
        current_index = lead_ids.index(lead_id.id)
        prev_id = lead_ids[current_index - 1] if current_index > 0 else None
        next_id = lead_ids[current_index + 1] if current_index < len(lead_ids) - 1 else None
        values = {
            'lead': lead_id,
            'prev_record': f'/my/lead/{prev_id}' if prev_id else None,
            'next_record': f'/my/lead/{next_id}' if next_id else None,
            'page_name': 'leads_form_view',

        }

        return request.render('website_property_mgmt.portal_my_leads_template_form_view', values)
