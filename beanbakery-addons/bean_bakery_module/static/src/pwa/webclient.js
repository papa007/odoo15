/** @odoo-module **/
import { WebClient } from "@web/webclient/webclient";
import { patch } from "web.utils";
// import {MyComponent} from '@bean_bakery_module/mycomponent'
var core = require("web.core");
var _t = core._t;
var swRegistration = null;
/**
 * to add, new function/ features to existing Odoo 15 component we use the patch function as following
 * Ex: patch([Component_name].prototype,"your_module_name.Your_Component_Name"){
 *    setup(){
 *      this._super();
 *      ... your code in super() ...
 *    }
 *
 *    ... Your code for new function/ feature ...
 * }
 */

patch(WebClient.prototype, "bean_bakery_module.BeanBakeryWebClient", {
  setup() {
    this._pwaregister();
    this._super();
  },
  _pwaregister()  {
    if ("serviceWorker" in navigator) {
      // register service worker
      navigator.serviceWorker
      .register("sw.js")
      .then((e) => this._onRegisterServiceWorker(e))
      .catch(function (error) {
        console.log(_t("[ServiceWorker] Registration failed: "), error);
      });
    } else {
      console.error(
        _t(
          "Service workers are not supported! Maybe you are not using HTTPS or you work in private mode."
        )
      );
    }
  },

  /**
   * Register service-worker success
   * Need register some extra API? override this!
   *
   * @private
   * @param {ServiceWorkerRegistration} registration
   */
  _onRegisterServiceWorker(registration) {
    const applicationServerKey =
      "BOJknxIjoq7dOWw5G_dhABviC7L4Nu6_mGUa9dBjtrK_k8rceMewnSJT70EApPyMZtV2gW65raOAO6JO0pOT6P4";
    console.log(_t("[ServiceWorker] Registered:"), registration);
    swRegistration = registration;
    //subcribe for push notification key
    swRegistration.pushManager
      .subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey,
      })
      .then(function (subscription) {
        console.log(_t("User is subscribed."), JSON.stringify(subscription));
      })
      .catch(function (err) {
        console.log(_t("Failed to subscribe the user: "), err);
      });
  },
});
