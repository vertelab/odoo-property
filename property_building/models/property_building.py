import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = 'contract.contract'

    related_property_id = fields.Many2one(comodel_name="property.property", string="Related property")

class PropertyContractWizard(models.TransientModel):
    _name = 'property.contract.wizard'
    _inherit = 'agreement.contract.wizard'
    _description = "Property contract wizard"

    _product_title = fields.Char(
        string="Product title",
        required=True,
    )

    cost_per_recurrance = fields.Float()

    def _get_product_title(self):
        _logger.warning("GOT PRODUCT TITLE")
        return self._product_title

    def _get_contract_name(self, _name):
        name = self._get_property().name
        product = self._get_product_title()
        return _("Contract for {} at {}").format(product, name)

    def _get_active_ids(self):
        return self.env.context.get('active_ids')

    def _get_current_agreement(self):
        try:
            domain = [('property_id', 'in', self._get_active_ids())]
            for property_model in self.env["agreement"].search(domain):
                return property_model
        except Exception as e:
            _logger.error(e)

    def _get_property(self):
        domain = [('id', 'in', self._get_active_ids())]
        return self.env['property.property'].search(domain)

    def store_contract_id(self, _, contract_id):
        self._get_property().write({
            'contract_ids': [(4, contract_id.id)],
        })


AREA = _('Area')
HECTARE = _('Hectare')
SQUARE_METER = _('Square meter')


def type_per_year(recurring_rule_type):
    if recurring_rule_type == "daily":
        return 1 / 365.2425  # TODO: Consider if this year is leap
    elif recurring_rule_type == "weekly":
        return 7 * type_per_year("daily")
    elif recurring_rule_type in ("monthly", "monthlylastday"):
        return 1 / 12
    elif recurring_rule_type == "quarterly":
        return 1 / 4
    elif recurring_rule_type == "semesterly":
        return 1 / 2
    else:
        return 1


def get_period(contract, contract_line):
    interesting = contract if contract.line_recurrence is False else contract_line

    period = interesting.recurring_rule_type
    interval = interesting.recurring_interval

    return type_per_year(period) * interval


def _create_uom_if_missing(environment):
    pass
    # ~ category = environment["uom.category"].sudo().search([('name', '=', AREA)])
    # ~ if not category:
        # ~ category = environment["uom.category"].sudo().create({
            # ~ 'name': AREA,
        # ~ })

    # ~ pre_defined = [
        # ~ {
            # ~ 'name': SQUARE_METER,
            # ~ 'category_id': category.id,
            # ~ 'uom_type': 'reference',
        # ~ },
        # ~ {
            # ~ 'name': HECTARE,
            # ~ 'category_id': category.id,
            # ~ 'uom_type': 'bigger',
            # ~ 'factor_inv': 10000,
        # ~ },
    # ~ ]

    # ~ for unit in pre_defined:
        # ~ if not environment["uom.uom"].sudo().search([('name', '=', unit['name'])]):
            # ~ environment["uom.uom"].sudo().create(unit)


class PropertyBuilding(models.Model):
    _inherit = 'property.property'

    def _create_uom(self):
        for rec in self:
            pass
            # ~ _create_uom_if_missing(self.env)
        self.compute_field = 0.0

    # ~ # TODO: Remove this and move create_uom to instansiation of module instead.
    # ~ compute_field = fields.Float(string="Compute field",)

  
    @api.depends("contract_ids", "contract_ids.contract_line_ids", "contract_ids.recurring_rule_type",
                 "contract_ids.recurring_interval")
    def _calculate_operating_cost(self):
        _logger.warning(f"Recalculating contract yerly cost! {len(self)}")
        for record in self:
            cost_per_year = 0
            try:
                for contract_id in record.contract_ids:
                    _logger.warning(f"{contract_id=}")
                    for contract_line in contract_id.contract_line_ids:
                        _logger.warning(f"{contract_line=}")
                        line_price = contract_line.price_unit * contract_line.quantity
                        period = get_period(contract_id, contract_line)
                        cost_per_year += line_price / period
            except (TypeError, ZeroDivisionError) as e:
                _logger.error(e)
            record.operating_cost = cost_per_year

    area_type = fields.Selection(        [
            ('apartment', 'Apartment'),
            ('commercial', 'Commercial'),
            ('garage', 'Garage'),
            ('industry', 'Industry'),
            ('office', 'Office'),
            ('parking', 'Parking'),
            ('public', 'Public Service'),
            ('residential', 'Residential'),
            ('storage', 'Storage space'),
            ('other', 'Other'),
        ],
        string="Area Type",
        required=True,
        default="other",
    )

    access_codes = fields.Text(string="Access code for properties",)
    bathrooms = fields.Integer(string="Bathrooms", help="Number of bathrooms in the property")
    charging_posts = fields.Integer(string="Charging posts",default=0,)
    district = fields.Char(string="District",)
    employees = fields.Integer(string="Employees",)
    floor = fields.Char(string="Floor",)
    garage_spaces = fields.Integer(string="Garage spaces",default=0,)
    kitchens = fields.Integer(string="Kitchen", help="Number of kitchens in the property")    
    municipality_id = fields.Many2one(comodel_name='res.country.municipality',string='Municipality')
    object_id = fields.Char(string="Object ID",)
    project_number = fields.Char(string="Object ID",)
    operating_cost = fields.Float(string="Operating Cost",compute="_calculate_operating_cost",)
    parking_spaces = fields.Integer(string="Parking spaces",default=0,)
    price = fields.Float(string="Price")
    property_state_id = fields.Many2one(comodel_name='res.country.state',string='State',domain=[('country_id.phone_code', '=', '46')],)
    bedrooms = fields.Integer(string="Rooms", help="Number of rooms in the property")    
    rooms = fields.Integer(string="Rooms", help="Number of rooms in the property")    
    workplaces = fields.Integer(string="Workplaces",)

    #TODO: hör denna hit?
    contract_ids = fields.One2many("contract.contract","related_property_id",string="Related Contracts",required=False,)

    def _get_hectare(self):
        _create_uom_if_missing(self.env)
        return self.env["uom.uom"].sudo().search([('name', '=', HECTARE)]).id

    size_uom = fields.Many2one(
        comodel_name="uom.uom",
        # TODO: use an 'Area' category, see odooext-skogsstyrelsen/migration_helper/models/mapping
        domain=f"[('category_id.name', '=', '{AREA}')]",
        default=_get_hectare,
    )

    # Additional information


    # TODO: Set everything to 0 when incorrect area_type
