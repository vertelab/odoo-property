from odoo import models, fields, api, _

class Project(models.Model):
    _inherit = "project.project"

    property_id = fields.Many2one("property.property", string="Property")
    is_property_project = fields.Boolean(string='Is Property Project',help="This is a project connected to a Property")
    is_property_task = fields.Boolean(string='Is Property Task',help="This is a project task connected to a Property")

class ProjectTask(models.Model):
    _inherit = "project.task"

    property_id = fields.Many2one("property.property", string="Property")



