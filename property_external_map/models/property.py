import logging

from odoo import _, api, models, fields
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    longitude = fields.Float(string='Geo Longitude', digits=(16, 5))

    property_lat_rt90 = fields.Float(string='Property Lat RT90', digits=(16, 5), related='latitude')
    property_long_rt90 = fields.Float(string='Property Long RT90', digits=(16, 5), related='longitude')
    property_lat_sweref99 = fields.Float(string='Property Lat SWEREF99', digits=(16, 5), related='latitude')
    property_long_sweref99 = fields.Float(string='Property Long SWEREF99', digits=(16, 5), related='longitude')
    property_lat_wgs8 = fields.Float(string='Property Lat WGS8', digits=(16, 5), related='latitude')
    property_long_wgs8 = fields.Float(string='Property Long WGS8', digits=(16, 5), related='longitude')

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(partner.street,
                                        partner.zip,
                                        partner.city,
                                        partner.state_id.name,
                                        partner.country_id.name)

            if result:
                partner.write({
                    'latitude': result[0],
                    'longitude': result[1],
                })
        return True

    def _address_as_string(self):
        self.ensure_one()
        addr = []
        if self.street:
            addr.append(self.street)
        if self.street2:
            addr.append(self.street2)
        if hasattr(self, "street3") and self.street3:
            addr.append(self.street3)
        if self.city:
            addr.append(self.city)
        if self.state_id:
            addr.append(self.state_id.name)
        if self.country_id:
            addr.append(self.country_id.name)
        if not addr:
            raise UserError(_("Address missing on partner '%s'.") % self.name)
        return " ".join(addr)

    @api.model
    def _prepare_url(self, url, replace):
        assert url, "Missing URL"
        for key, value in replace.items():
            if not isinstance(value, str):
                # for latitude and longitude which are floats
                if isinstance(value, float):
                    value = "%.5f" % value
                else:
                    value = ""
            url = url.replace(key, value)
        logger.debug("Final URL: %s", url)
        return url

    def open_map(self):
        self.ensure_one()
        map_website = self.env.user.context_map_website_id
        if not map_website:
            raise UserError(
                _("Missing map provider: " "you should set it in your preferences.")
            )
        # Since v13, fields partner_latitude and partner_longitude are
        # in the "base" module
        if map_website.lat_lon_url and self.latitude and self.longitude:
            url = self._prepare_url(
                map_website.lat_lon_url,
                {
                    "{LATITUDE}": self.latitude,
                    "{LONGITUDE}": self.longitude,
                },
            )
        else:
            if not map_website.address_url:
                raise UserError(
                    _(
                        "Missing parameter 'URL that uses the address' "
                        "for map website '%s'."
                    )
                    % map_website.name
                )
            url = self._prepare_url(
                map_website.address_url, {"{ADDRESS}": self._address_as_string()}
            )
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
