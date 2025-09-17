# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyImages(models.Model):
    _name = 'property.image'
    _description = 'Property Images'

    name = fields.Char(string='Name', required=True, help='Name for the given image')
    description = fields.Text(string='Description', help='A brief description of the image given')
    image_1024 = fields.Image("Property Image", max_width=1024, max_height=1024)
    property_id = fields.Many2one('property.property', string='Property', help='Related property')