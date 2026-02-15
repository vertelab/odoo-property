from odoo import api, fields, models

class MailActivityTypeResModel(models.Model):
    _inherit = "mail.activity.type"

    res_model_id = fields.Many2one('ir.model', 'Document Model', index=True, ondelete='cascade', required=True)

