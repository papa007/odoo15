# Copyright 2022 Anhjean
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Progressive web application",
    "summary": "Bean Bakery PWA",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://beanbakery.vn/dev",
    "author": "Anhjean - Bean Bakery",
    "maintainers": ["Anhjean"],
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "depends": ["web", "mail"],
    "data": ["templates/assets.xml", "views/res_config_settings_views.xml"],
    "images": ["static/description/pwa.png"],
    'assets': {
        'web.assets_backend': [
            "/beanbakery_pwa/static/src/webclient.js",
        ],
    },
}
