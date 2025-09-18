from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class PropertyProperty(models.Model):
    _name = 'property.property'
    _inherit = [
        'property.property',
        'website.seo.metadata',
        'website.published.multi.mixin',
        'website.cover_properties.mixin',
        'website.searchable.mixin',
    ]

    #TODO: Dangerous dependense on website_event do we need that?
    def _default_cover_properties(self):
        res = super()._default_cover_properties()
        res.update({
            'background-image': "url('/website_event/static/src/img/event_cover_4.jpg')",
            'opacity': '0.4',
            'resize_class': 'cover_auto'
        })
        return res

    # website
    is_visible_on_website = fields.Boolean(string="Visible On Website", compute='_compute_is_visible_on_website',
                                           search='_search_is_visible_on_website')
    website_visibility = fields.Selection(
        [('public', 'Public'), ('link', 'Via a Link'), ('logged_users', 'Logged Users')],
        string="Website Visibility", required=True, default='public', tracking=True,
        help="""Defines the Visibility of the Event on the Website and searches.\n
            Note that the Event is however always available via its link.""")
    website_published = fields.Boolean(tracking=True)
    property_image_ids = fields.One2many("property.image", "property_id", string="Property Images")

    @api.depends('stakeholder_ids')
    def _compute_agent_stakeholder(self):
        for rec in self:
            if rec.stakeholder_ids:
                agent_stakeholder = rec.stakeholder_ids.filtered(
                    lambda stakeholder: stakeholder.partner_status == 'agent' and stakeholder.id
                )
                if agent_stakeholder:
                    rec.agent_stakeholder_id = agent_stakeholder[0].partner_id.id
                else:
                    rec.agent_stakeholder_id = False
            else:
                rec.agent_stakeholder_id = False

    agent_stakeholder_id = fields.Many2one("res.partner", string="Agent", compute=_compute_agent_stakeholder, store=True)

    @api.depends_context('uid')
    @api.depends('website_visibility')
    def _compute_is_visible_on_website(self):
        if all(event.website_visibility == 'public' for event in self):
            self.is_visible_on_website = True
            return
        for event in self:
            if event.website_visibility == 'public':
                event.is_visible_on_website = True
            elif not self.env.user._is_public() and event.website_visibility == 'logged_users':
                event.is_visible_on_website = True
            else:
                event.is_visible_on_website = False

    #TODO: Looks wrong
    @api.model
    def _search_is_visible_on_website(self, operator, value):
        if operator not in ['=', '!=']:
            raise NotImplementedError(_('This operator is not supported'))
        if not isinstance(value, bool):
            raise UserError(_('Value should be True or False (not %)', value))
        check_is_visible_on_website = operator == '=' and value or operator == '!=' and not value
        user = self.env.user
        domain = [('is_participating', '=', True)]

        if not user._is_public():
            domain = expression.OR([domain, [('website_visibility', 'in', ['public', 'logged_users'])]])
        else:
            domain = expression.OR([domain, [('website_visibility', '=', 'public')]])

        event_ids = self.env['event.event']._search(domain)
        return [('id', 'in' if check_is_visible_on_website else 'not in', event_ids)]

    @api.depends('name')
    def _compute_website_url(self):
        super(PropertyProperty, self)._compute_website_url()
        for property in self:
            if property.id:  # avoid to perform a slug on a not yet saved record in case of an onchange.
                property.website_url = '/property/%s' % self.env['ir.http']._slug(property)
