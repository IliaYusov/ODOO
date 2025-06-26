/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { PartnerKanbanController } from "./partner_kanban_controller";

export const PartnerKanbanView = {
    ...kanbanView,
    Controller: PartnerKanbanController,
    buttonTemplate: "partner_dadata.KanbanViewButtons"
};

registry.category("views").add("partner_kanban", PartnerKanbanView);
