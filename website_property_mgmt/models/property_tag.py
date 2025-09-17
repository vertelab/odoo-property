from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'Property Tag'

    name = fields.Char(string='Tag', required=True, help='Name of the tag')

    _sql_constraints = [
        ('tag_name_uniq', 'unique (name)', "Tag name already exists!"),
    ]