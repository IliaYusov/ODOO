/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { sprintf } from 'web.utils';

export class SubtaskCounter extends Component {
    get closedSubtaskCount() {
        return this.props.record.data.closed_subtask_count;
    }

    get subtaskCount() {
        return this.props.record.data.subtask_count;
    }

    get counterTitle() {
        return sprintf(_t("%s sub-tasks closed out of %s"), this.closedSubtaskCount, this.subtaskCount);
    }

    get counterDisplay() {
        return sprintf(_t("%s/%s"), this.closedSubtaskCount, this.subtaskCount);
    }
}
SubtaskCounter.template = "task.SubtaskCounter";
SubtaskCounter.props = {
    ...standardWidgetProps
};
SubtaskCounter.fieldDependencies = {
    subtask_count: { type: "integer" },
    closed_subtask_count: { type: "integer" }
};

registry.category("view_widgets").add("subtask_counter", SubtaskCounter);
