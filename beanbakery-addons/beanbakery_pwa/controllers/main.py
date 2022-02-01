# Copyright 2020 Lorenzo Battistini @ TAKOBI
# Copyright 2020 Tecnativa - Alexandre D. Díaz
# Copyright 2020 Tecnativa - João Marques
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import json

from odoo.http import Controller, request, route


class PWA(Controller):
    def _get_pwa_scripts(self):
        """Scripts to be imported in the service worker (Order is important)
            for odoo 15 all legacy script is in the '/web/static/src/legacy' folder
            Due to this 
        """
        return [
            "/web/static/lib/underscore/underscore.js",
            "/beanbakery_pwa/static/src/worker/jquery-sw-compat.js",
            "/web/static/src/legacy/js/promise_extension.js",
            "/web/static/src/boot.js",
            "/web/static/src/legacy/js/core/class.js",
            "/beanbakery_pwa/static/src/worker/pwa.js",
        ]

    @route("/service-worker.js", type="http", auth="public")
    def render_service_worker(self):
        """Route to register the service worker in the 'main' scope ('/')"""
        return request.render(
            "beanbakery_pwa.service_worker",
            {
                "pwa_scripts": self._get_pwa_scripts(),
                "pwa_params": self._get_pwa_params(),
            },
            headers=[("Content-Type", "text/javascript;charset=utf-8")],
        )

    def _get_pwa_params(self):
        """Get javascript PWA class initialzation params"""
        return {}

    def _get_pwa_manifest_icons(self, pwa_icon):
        icons = []
        if not pwa_icon:
            for size in [
                (128, 128),
                (144, 144),
                (152, 152),
                (192, 192),
                (256, 256),
                (512, 512),
            ]:
                icons.append(
                    {
                        "src": "/beanbakery_pwa/static/img/icons/icon-%sx%s.png"
                        % (str(size[0]), str(size[1])),
                        "sizes": "{}x{}".format(str(size[0]), str(size[1])),
                        "type": "image/png",
                        "purpose": "any",
                    }
                )
        elif not pwa_icon.mimetype.startswith("image/svg"):
            all_icons = (
                request.env["ir.attachment"]
                .sudo()
                .search(
                    [
                        ("url", "like", "/beanbakery_pwa/icon"),
                        (
                            "url",
                            "not like",
                            "/beanbakery_pwa/icon.",
                        ),  # Get only resized icons
                    ]
                )
            )
            for icon in all_icons:
                icon_size_name = icon.url.split("/")[-1].lstrip("icon").split(".")[0]
                icons.append(
                    {"src": icon.url, "sizes": icon_size_name, "type": icon.mimetype,"purpose": "any"}
                )
        else:
            icons = [
                {
                    "src": pwa_icon.url,
                    "sizes": "128x128 144x144 152x152 192x192 256x256 512x512",
                    "type": pwa_icon.mimetype,
                    "purpose": "any",
                }
            ]
        return icons

    def _get_pwa_manifest(self):
        """Webapp manifest"""
        config_param_sudo = request.env["ir.config_parameter"].sudo()
        pwa_name = config_param_sudo.get_param("pwa.manifest.name", "Bean Bakery PWA")
        pwa_short_name = config_param_sudo.get_param(
            "pwa.manifest.short_name", "BeanBakery PWA"
        )
        pwa_icon = (
            request.env["ir.attachment"]
            .sudo()
            .search([("url", "like", "/beanbakery_pwa/icon.")])
        )
        background_color = config_param_sudo.get_param(
            "pwa.manifest.background_color", " #addbc5"
        )
        theme_color = config_param_sudo.get_param("pwa.manifest.theme_color", " #addbc5")
        return {
            "name": pwa_name,
            "short_name": pwa_short_name,
            "icons": self._get_pwa_manifest_icons(pwa_icon),
            "id": "/web",
            "start_url": "/web",
            "display": "standalone",
            "orientation": "any",
            "background_color": background_color,
            "theme_color": theme_color,
        }

    @route("/beanbakery_pwa/manifest.webmanifest", type="http", auth="public")
    def pwa_manifest(self):
        """Returns the manifest used to install the page as app"""
        return request.make_response(
            json.dumps(self._get_pwa_manifest()),
            headers=[("Content-Type", "application/json;charset=utf-8")],
        )
