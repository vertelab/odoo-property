import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


#TODO: Move these to their own model.
class PropertyContract(models.Model):
    _inherit = 'contract.contract'

    related_property_id = fields.Many2one("property.property", string="Related property")


#TODO: Move these to their own model.
class PropertyContractWizard(models.TransientModel):
    _name = 'property.contract.wizard'
    _inherit = 'agreement.contract.wizard'
    _description = "Property contract wizard"

    _product_title = fields.Char(
            string="Product title",
            required=True,
            )

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
SQUARE_METER= _('Square meter')


def type_per_year(recurring_rule_type):
    if recurring_rule_type == "daily":
        return 1/365.2425 # TODO: Consider if this year is leap
    elif recurring_rule_type == "weekly":
        return 7 * type_per_year("daily")
    elif recurring_rule_type in ("monthly", "monthlylastday"):
        return 1/12
    elif recurring_rule_type == "quarterly":
        return 1/4
    elif recurring_rule_type == "semesterly":
        return 1/2
    else:
        return 1


def get_period(contract, contract_line):
    interesting = contract if contract.line_recurrence is False else contract_line

    period = interesting.recurring_rule_type
    interval = interesting.recurring_interval

    return type_per_year(period) * interval


def _create_uom_if_missing(environment):
    category = environment["uom.category"].sudo().search([('name', '=', AREA)])
    if not category:
        category = environment["uom.category"].sudo().create({
            'name': AREA,
            })

    pre_defined = [
            {
                'name': SQUARE_METER,
                'category_id': category.id,
                'uom_type': 'reference',
                },
            {
                'name': HECTARE,
                'category_id': category.id,
                'uom_type': 'bigger',
                'factor_inv': 10000,
                },
            ]

    for unit in pre_defined:
        if not environment["uom.uom"].sudo().search([('name', '=', unit['name'])]):
            environment["uom.uom"].sudo().create(unit)


class PropertyBuilding(models.Model):
    _description = "Property Building"
    _inherit = 'property.property'

    def __init__(self, *args, **kwargs):
        super(PropertyBuilding, self).__init__(*args, **kwargs)

    def _create_uom(self):
        for rec in self:
            _create_uom_if_missing(self.env)
        self.compute_field = 0.0

    # TODO: Remove this and move create_uom to instansiation of module instead.
    compute_field = fields.Float(string="Compute field", compute=_create_uom)

    # TODO: Make this calculated from contract_ids.
    operating_cost = fields.Float(
            string="Operating Cost",
            compute="_calculate_operating_cost",
            )

    access_codes = fields.Text(
            string="Access code for properties",
            )

    parking_spaces = fields.Integer(
            string="Parking spaces",
            default=0,
            )

    garage_spaces = fields.Integer(
            string="Garage spaces",
            default=0,
            )

    charging_posts = fields.Integer(
            string="Charging posts",
            default=0,
            )

    @api.depends("contract_ids", "contract_ids.contract_line_ids", "contract_ids.recurring_rule_type", "contract_ids.recurring_interval")
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

    ## 3. Lokalens adress
    municipality_id = fields.Many2one(
            comodel_name='res.country.municipality',
            # TODO: Create domain for this that limits municipality depending on the choosen district
            string='Municipality'
            )

    property_state_id = fields.Many2one(
            comodel_name='res.country.state',
            string='State',
            # TODO: Extend this to be able to select from non-swedish places (and dont identify via phone_code)...
            domain=[('country_id.phone_code', '=', '46')],
            )

    district = fields.Char(
            string="District",
            )

    # TODO: make sure this only contains numbers
    project_number = fields.Char(
            string="Project (Office) ID",
            )

    @api.constrains('project_number')
    def _check_only_contains_numbers(self):
        if self.project_number and not self.project_number.isdecimal():
            raise ValidationError(_("Only numbers allowed in Project ID"))

    # TODO: Create region data, enable this and add it to views.
    #region_id = fields.Many2one(
    #        comodel_name='res.country.region',
    #        string="Region",
    #        )

    ## 8. Area
    area_type = fields.Selection(
            [
                ('office', 'Office'),
                ('storage', 'Storage space'),
                ('mechanic', 'Mechanic'),
                ('parking', 'Parking'),
                ('garage', 'Garage'),
                ('other', 'Other'),
                ],
            string="Area Type",
            required=True,
            default="other",
            )

    floor = fields.Char(
            string="Floor",
            )

    contract_ids = fields.One2many(
            "contract.contract",
            "related_property_id",
            string="Related Contracts",
            required=False,
            )

    def _get_hectare(self):
        _create_uom_if_missing(self.env)
        return self.env["uom.uom"].sudo().search([('name', '=', HECTARE)]).id

    size_uom = fields.Many2one(
            comodel_name="uom.uom",
            #TODO: use an 'Area' category, see odooext-skogsstyrelsen/migration_helper/models/mapping
            domain=f"[('category_id.name', '=', '{AREA}')]",
            default=_get_hectare,
            )

    ## Additional information

    employees = fields.Integer(
            string="Employees",
            )

    workplaces = fields.Integer(
            string="Workplaces",
            )


    # TODO: Set everything to 0 when incorrect area_type
