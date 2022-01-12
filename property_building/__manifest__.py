
{
    "name": "Property - Building",
    "summary": "Adds new variables to property model, useful for buildings",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "TODO",
    "author": "Emanuel Bergsten",
    "maintainers": ["Vertelab"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "contract",
        "agreement_contract",
        "property_mgmt",
        "l10n_se_municipality_class",
    ],
    "data": [
        "views/property_building.xml",
        "security/ir.model.access.csv",
    ],
}
