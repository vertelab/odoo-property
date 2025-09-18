from odoo import models, fields, api, _
import requests
import json
from datetime import datetime
import ast


class Maintenance(models.Model):
    _inherit = "maintenance.equipment"
    property_id = fields.Many2one("property.property", string="Property")



