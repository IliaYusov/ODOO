/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";

export class PartnerKanbanController extends KanbanController {
    setup() {
        super.setup();
    }

    loadPartner() {
        this.actionService.doAction({
            name: this.env._t("Create Partner"),
            type: "ir.actions.act_window",
            res_model: "partner.load.info",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new"
        });
    };
}
