/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { routeToUrl } from "@web/core/browser/router_service";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "base_custom_app.UserMenu", {
    setup() {
        "use strict";
        this._super.apply(this, arguments);

        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
        userMenuRegistry.remove("odoo_account");
        if (session.show_documentation) {
            userMenuRegistry.add("documentation", documentationItem, {'force': true});
        }
    }
});

function documentationItem(env) {
    return {
        type: "item",
        id: "documentation",
        description: env._t("Documentation"),
        callback: async function () {
            const actionDescription = await env.services.orm.call("knowledge.article", "action_get");
            env.services.action.doAction(actionDescription);
        },
        sequence: 10
    };
}
