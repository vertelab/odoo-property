from odoo import models, fields, api, _
import requests
import json
from datetime import datetime
import ast


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"

    property_id = fields.Many2one("property.property", string="Property")



