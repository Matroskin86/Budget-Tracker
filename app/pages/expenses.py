import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.empty_state import empty_state
from app.states.budget_state import BudgetState, Expense, ExpenseSplit
from app.states.team_state import TeamState


def tab_button(id: str, label: str, icon: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, size=16, class_name="mr-2"),
        rx.el.span(label),
        on_click=lambda: BudgetState.set_active_expense_tab(id),
        class_name=rx.cond(
            BudgetState.active_expense_tab == id,
            "flex items-center px-4 py-2 text-sm font-medium text-indigo-600 border-b-2 border-indigo-600 bg-indigo-50/50",
            "flex items-center px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 border-b-2 border-transparent transition-colors",
        ),
    )


def get_tag_badge_class(tag: str) -> rx.Component:
    return rx.match(
        tag,
        (
            "Travel",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-sky-50 text-sky-700 border-sky-100",
        ),
        (
            "Food",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-orange-50 text-orange-700 border-orange-100",
        ),
        (
            "Equipment",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-slate-50 text-slate-700 border-slate-200",
        ),
        (
            "Software",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-indigo-50 text-indigo-700 border-indigo-100",
        ),
        (
            "Office",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-stone-50 text-stone-700 border-stone-200",
        ),
        (
            "Client",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-purple-50 text-purple-700 border-purple-100",
        ),
        (
            "Internal",
            "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-gray-50 text-gray-700 border-gray-200",
        ),
        "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border bg-gray-50 text-gray-700 border-gray-200",
    )


def tag_badge(tag: str, on_remove: rx.event.EventType = None) -> rx.Component:
    return rx.el.span(
        tag,
        rx.cond(
            on_remove != None,
            rx.el.button(
                rx.icon("x", size=12),
                on_click=on_remove,
                class_name="ml-1.5 hover:text-red-500 transition-colors",
            ),
        ),
        class_name=get_tag_badge_class(tag),
    )


def expense_details_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Description", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.input(
                on_change=lambda val: BudgetState.update_current_expense(
                    "description", val
                ),
                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                placeholder="What was this for?",
                default_value=BudgetState.current_expense["description"],
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Amount", class_name="block text-sm font-medium text-gray-700 mb-1"
                ),
                rx.el.input(
                    type="number",
                    on_change=lambda val: BudgetState.update_current_expense(
                        "amount", val
                    ),
                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                    default_value=BudgetState.current_expense["amount"],
                ),
                class_name="col-span-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Date", class_name="block text-sm font-medium text-gray-700 mb-1"
                ),
                rx.el.input(
                    type="date",
                    on_change=lambda val: BudgetState.update_current_expense(
                        "date", val
                    ),
                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                    default_value=BudgetState.current_expense["date"],
                ),
                class_name="col-span-1",
            ),
            class_name="grid grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Category",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.foreach(
                        BudgetState.budgets,
                        lambda b: rx.el.option(b["name"], value=b["name"]),
                    ),
                    value=BudgetState.current_expense["category"],
                    on_change=lambda val: BudgetState.update_current_expense(
                        "category", val
                    ),
                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                ),
                class_name="col-span-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Payment Method",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Credit Card", value="Credit Card"),
                    rx.el.option("Bank Transfer", value="Bank Transfer"),
                    rx.el.option("Invoice", value="Invoice"),
                    rx.el.option("Reimbursement", value="Reimbursement"),
                    rx.el.option("Cash", value="Cash"),
                    value=BudgetState.current_expense["payment_method"],
                    on_change=lambda val: BudgetState.update_current_expense(
                        "payment_method", val
                    ),
                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                ),
                class_name="col-span-1",
            ),
            class_name="grid grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Tags", class_name="block text-sm font-medium text-gray-700 mb-2"
            ),
            rx.el.div(
                rx.foreach(
                    BudgetState.current_expense["tags"],
                    lambda tag: tag_badge(
                        tag,
                        on_remove=lambda: BudgetState.remove_tag_from_current_expense(
                            tag
                        ),
                    ),
                ),
                class_name="flex flex-wrap gap-2 mb-2 min-h-[24px]",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Add a tag...", value=""),
                    rx.foreach(
                        BudgetState.available_tags, lambda t: rx.el.option(t, value=t)
                    ),
                    on_change=BudgetState.add_tag_to_current_expense,
                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border text-sm",
                )
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Recurring Frequency",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.select(
                rx.el.option("One-time", value="One-time"),
                rx.el.option("Weekly", value="Weekly"),
                rx.el.option("Monthly", value="Monthly"),
                rx.el.option("Quarterly", value="Quarterly"),
                rx.el.option("Annual", value="Annual"),
                value=BudgetState.current_expense["recurring_frequency"],
                on_change=lambda val: BudgetState.update_current_expense(
                    "recurring_frequency", val
                ),
                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=BudgetState.current_expense["has_attachment"],
                        on_change=BudgetState.toggle_current_expense_attachment,
                        class_name="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 h-4 w-4 mr-2",
                    ),
                    rx.el.span(
                        "Receipt / Attachment Included",
                        class_name="text-sm text-gray-700",
                    ),
                    class_name="flex items-center cursor-pointer",
                ),
                rx.cond(
                    BudgetState.current_expense["has_attachment"],
                    rx.el.div(
                        rx.el.button(
                            "Preview",
                            on_click=BudgetState.open_attachment_preview,
                            class_name="text-xs text-indigo-600 font-medium hover:underline",
                        ),
                        rx.cond(
                            BudgetState.current_expense["attachment_url"] != "",
                            rx.image(
                                src=BudgetState.current_expense["attachment_url"],
                                class_name="w-8 h-8 rounded object-cover border border-gray-200 ml-2 cursor-pointer hover:opacity-80",
                                on_click=BudgetState.open_attachment_preview,
                            ),
                        ),
                        class_name="flex items-center ml-auto",
                    ),
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            class_name="p-3 bg-gray-50 rounded-lg border border-gray-200 mb-4",
        ),
    )


def split_row(split: ExpenseSplit, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    BudgetState.budgets,
                    lambda b: rx.el.option(b["name"], value=b["name"]),
                ),
                value=split["category"],
                on_change=lambda val: BudgetState.update_split(index, "category", val),
                class_name="w-full rounded-lg border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500 border px-2 py-1.5",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.input(
                type="number",
                on_change=lambda val: BudgetState.update_split(index, "amount", val),
                class_name="w-full rounded-lg border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500 border px-2 py-1.5",
                placeholder="0.00",
                default_value=split["amount"],
            ),
            class_name="w-24",
        ),
        rx.el.button(
            rx.icon("trash-2", size=16),
            on_click=lambda: BudgetState.remove_split(index),
            class_name="text-gray-400 hover:text-red-500 p-2",
        ),
        class_name="flex items-center gap-2 mb-2",
    )


def expense_splits_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Split this expense across multiple categories.",
                class_name="text-sm text-gray-500 mb-4",
            ),
            rx.foreach(
                BudgetState.current_expense["splits"], lambda s, i: split_row(s, i)
            ),
            rx.el.button(
                "+ Add Split",
                on_click=BudgetState.add_split,
                class_name="text-sm font-medium text-indigo-600 hover:text-indigo-800 mt-2",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Total Split:", class_name="text-sm text-gray-600"),
                rx.el.span(
                    f"${BudgetState.current_split_total:,.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
                class_name="flex justify-between font-medium pt-4 border-t border-gray-100",
            ),
            rx.cond(
                BudgetState.split_difference != 0,
                rx.el.div(
                    rx.el.span("Difference:", class_name="text-sm text-gray-600"),
                    rx.el.span(
                        f"${BudgetState.split_difference:,.2f}",
                        class_name="text-sm font-bold text-red-500",
                    ),
                    class_name="flex justify-between font-medium mt-2",
                ),
            ),
        ),
    )


def expense_comments_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                BudgetState.current_expense["comments"],
                lambda comment: rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={comment['avatar']}",
                            class_name="w-8 h-8 rounded-full bg-gray-100 border border-gray-200",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    comment["user"],
                                    class_name="text-xs font-bold text-gray-900 mr-2",
                                ),
                                rx.el.span(
                                    comment["timestamp"],
                                    class_name="text-[10px] text-gray-400",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.p(
                                comment["text"], class_name="text-sm text-gray-700"
                            ),
                            class_name="flex-1 bg-gray-50 p-3 rounded-xl rounded-tl-none",
                        ),
                        class_name="flex gap-3 mb-4",
                    )
                ),
            ),
            rx.cond(
                BudgetState.current_expense["comments"].length() == 0,
                rx.el.p(
                    "No comments yet.",
                    class_name="text-center text-sm text-gray-400 py-4 italic",
                ),
            ),
            class_name="max-h-[250px] overflow-y-auto mb-4 custom-scrollbar px-1",
        ),
        rx.el.div(
            rx.el.textarea(
                placeholder="Add a note or comment...",
                on_change=BudgetState.set_new_comment_text,
                class_name="w-full rounded-lg border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500 border px-3 py-2 min-h-[80px] mb-2",
                default_value=BudgetState.new_comment_text,
            ),
            rx.el.button(
                "Post Comment",
                on_click=BudgetState.add_expense_comment,
                class_name="px-3 py-1.5 bg-gray-900 text-white text-xs font-medium rounded-lg hover:bg-gray-800 ml-auto block",
            ),
        ),
    )


def expense_approval_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Approval Status",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.select(
                rx.el.option("Pending", value="Pending"),
                rx.el.option("Approved", value="Approved"),
                rx.el.option("Rejected", value="Rejected"),
                value=BudgetState.current_expense["approval_status"],
                on_change=lambda val: BudgetState.update_current_expense(
                    "approval_status", val
                ),
                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Assigned Approver",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.select(
                rx.el.option("Select Approver...", value=""),
                rx.foreach(
                    TeamState.team_members,
                    lambda m: rx.el.option(m["name"], value=m["id"]),
                ),
                value=BudgetState.current_expense["assigned_approver_id"],
                on_change=lambda val: BudgetState.update_current_expense(
                    "assigned_approver_id", val
                ),
                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
            ),
            class_name="mb-6",
        ),
    )


def expense_history_tab() -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            "Activity Log",
            class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4",
        ),
        rx.el.div(
            rx.foreach(
                BudgetState.current_expense["history"],
                lambda item: rx.el.div(
                    rx.el.div(
                        rx.icon(
                            rx.match(
                                item["action"],
                                ("Created", "plus"),
                                ("Approved", "check"),
                                ("Rejected", "x"),
                                ("Updated", "pencil"),
                                "clock",
                            ),
                            size=14,
                            class_name="text-gray-600",
                        ),
                        class_name="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center shrink-0 border border-gray-200 z-10",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                item["user"], class_name="font-semibold text-gray-900"
                            ),
                            rx.el.span(
                                f" {item['action']}",
                                class_name="text-sm text-gray-600 ml-1",
                            ),
                            class_name="flex items-baseline",
                        ),
                        rx.el.p(
                            item["note"],
                            class_name="text-xs text-gray-500 italic mt-0.5",
                        ),
                        rx.el.span(
                            item["timestamp"],
                            class_name="text-[10px] text-gray-400 block mt-1",
                        ),
                        class_name="bg-gray-50/50 rounded-lg p-3 w-full border border-gray-100",
                    ),
                    class_name="flex gap-4 mb-6 relative last:mb-0 before:absolute before:left-[15px] before:top-8 before:bottom-[-24px] before:w-[2px] before:bg-gray-100 last:before:hidden",
                ),
            ),
            rx.cond(
                BudgetState.current_expense["history"].length() == 0,
                rx.el.div(
                    rx.icon("history", size=48, class_name="text-gray-200 mb-2"),
                    rx.el.p(
                        "No history recorded yet.",
                        class_name="text-sm text-gray-500 font-medium",
                    ),
                    class_name="flex flex-col items-center justify-center py-12",
                ),
            ),
            class_name="max-h-[300px] overflow-y-auto pr-2 custom-scrollbar",
        ),
    )


def attachment_preview_modal() -> rx.Component:
    return rx.cond(
        BudgetState.is_attachment_preview_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/90 backdrop-blur-md transition-opacity z-[60]",
                on_click=BudgetState.close_attachment_preview,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Receipt Preview", class_name="text-white font-medium"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.button(
                                rx.icon("minus", size=16, class_name="text-white"),
                                on_click=BudgetState.zoom_out,
                                class_name="p-2 hover:bg-white/10 rounded-full transition-colors",
                            ),
                            rx.el.span(
                                f"{BudgetState.attachment_zoom}%",
                                class_name="text-white text-xs font-mono w-12 text-center",
                            ),
                            rx.el.button(
                                rx.icon("plus", size=16, class_name="text-white"),
                                on_click=BudgetState.zoom_in,
                                class_name="p-2 hover:bg-white/10 rounded-full transition-colors",
                            ),
                            class_name="flex items-center bg-black/40 rounded-full px-1 mr-4 border border-white/10",
                        ),
                        rx.el.a(
                            rx.icon(
                                "download",
                                size=20,
                                class_name="text-white hover:text-gray-200 transition-colors mr-4",
                            ),
                            href=BudgetState.current_expense["attachment_url"],
                            target="_blank",
                            download="receipt",
                        ),
                        rx.el.button(
                            rx.icon("x", size=24, class_name="text-white"),
                            on_click=BudgetState.close_attachment_preview,
                            class_name="hover:bg-white/10 p-1 rounded-lg transition-colors",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center mb-6 z-[80] relative",
                ),
                rx.el.div(
                    rx.image(
                        src=BudgetState.current_expense["attachment_url"],
                        class_name="rounded-lg shadow-2xl transition-transform duration-200 ease-out",
                        style={
                            "transform": f"scale({BudgetState.attachment_zoom / 100})",
                            "maxHeight": "75vh",
                            "maxWidth": "100%",
                        },
                    ),
                    class_name="flex items-center justify-center overflow-hidden h-[75vh] w-full",
                    on_click=BudgetState.close_attachment_preview,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[70] max-w-5xl w-full p-6",
            ),
        ),
    )


def expense_modal() -> rx.Component:
    return rx.cond(
        BudgetState.is_expense_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity",
                on_click=BudgetState.close_expense_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        rx.cond(
                            BudgetState.current_expense["id"],
                            "Edit Expense",
                            "Log Expense",
                        ),
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-400"),
                        on_click=BudgetState.close_expense_modal,
                        class_name="hover:bg-gray-100 p-1 rounded-full transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    tab_button("details", "Details", "file-text"),
                    tab_button("splits", "Splits", "split"),
                    tab_button("comments", "Comments", "message-square"),
                    tab_button("approval", "Approval", "circle_check_big"),
                    tab_button("history", "History", "history"),
                    class_name="flex space-x-1 border-b border-gray-200 mb-6 overflow-x-auto",
                ),
                rx.cond(
                    BudgetState.active_expense_tab == "details", expense_details_tab()
                ),
                rx.cond(
                    BudgetState.active_expense_tab == "splits", expense_splits_tab()
                ),
                rx.cond(
                    BudgetState.active_expense_tab == "comments", expense_comments_tab()
                ),
                rx.cond(
                    BudgetState.active_expense_tab == "approval", expense_approval_tab()
                ),
                rx.cond(
                    BudgetState.active_expense_tab == "history", expense_history_tab()
                ),
                rx.el.div(
                    rx.cond(
                        BudgetState.current_expense["id"],
                        rx.el.div(
                            rx.el.button(
                                rx.icon("copy", size=16),
                                on_click=lambda: BudgetState.duplicate_expense(
                                    BudgetState.current_expense
                                ),
                                class_name="p-2 text-gray-400 hover:text-indigo-600 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                                title="Duplicate",
                            ),
                            rx.el.button(
                                rx.icon("trash-2", size=16),
                                on_click=lambda: BudgetState.delete_expense(
                                    BudgetState.current_expense["id"]
                                ),
                                class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                                title="Delete",
                            ),
                            class_name="flex items-center mr-auto",
                        ),
                    ),
                    rx.el.button(
                        "Cancel",
                        on_click=BudgetState.close_expense_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-3",
                    ),
                    rx.el.button(
                        "Save Expense",
                        on_click=BudgetState.save_expense,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700",
                    ),
                    class_name="flex justify-end items-center pt-4 border-t border-gray-100 mt-2",
                ),
                class_name="relative bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 z-50 animate-in fade-in zoom-in duration-200",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
        rx.el.div(),
    )


def status_badge_full(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Approved",
            rx.el.span(
                "Approved",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
        ),
        (
            "Pending",
            rx.el.span(
                "Pending",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
        ),
        (
            "Rejected",
            rx.el.span(
                "Rejected",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
        ),
        rx.el.span(
            status,
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def expense_row_actions(expense: Expense) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.input(
                type="checkbox",
                checked=BudgetState.selected_expense_ids.contains(expense["id"]),
                on_change=lambda: BudgetState.toggle_expense_selection(expense["id"]),
                class_name="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 h-4 w-4",
            ),
            class_name="px-6 py-4 whitespace-nowrap w-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    expense["date"],
                    class_name="text-sm font-medium text-gray-900 block",
                ),
                rx.cond(
                    expense.get("recurring_frequency", "One-time") != "One-time",
                    rx.el.div(
                        rx.icon("repeat", size=12, class_name="text-indigo-500 mr-1"),
                        rx.el.span(
                            expense.get("recurring_frequency"),
                            class_name="text-[10px] text-indigo-600 font-medium",
                        ),
                        class_name="flex items-center mt-0.5",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                expense["category"],
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-lg text-xs font-medium bg-indigo-50 text-indigo-700",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        expense["description"],
                        class_name="text-sm text-gray-600 truncate",
                    ),
                    rx.cond(
                        expense.get("has_attachment", False),
                        rx.icon(
                            "paperclip",
                            size=14,
                            class_name="text-gray-400 ml-2 shrink-0",
                        ),
                    ),
                    class_name="flex items-center max-w-[250px]",
                ),
                rx.cond(
                    expense.get("tags", []).length() > 0,
                    rx.el.div(
                        rx.foreach(expense.get("tags", []), lambda tag: tag_badge(tag)),
                        class_name="flex gap-1 mt-1 flex-wrap",
                    ),
                ),
                rx.cond(
                    expense["splits"].length() > 0,
                    rx.el.div(
                        rx.icon("split", size=12, class_name="text-indigo-500"),
                        rx.el.span(
                            "Split",
                            class_name="text-[10px] text-indigo-600 font-medium ml-1",
                        ),
                        class_name="flex items-center mt-1 bg-indigo-50 w-fit px-1.5 py-0.5 rounded",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                f"${expense['amount']:,.2f}",
                class_name="text-sm font-bold text-gray-900",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(expense["payment_method"], class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge_full(expense["approval_status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "pencil",
                        size=16,
                        class_name="text-gray-400 hover:text-indigo-600",
                    ),
                    on_click=lambda: BudgetState.open_edit_expense_modal(expense),
                    class_name="p-1 hover:bg-gray-100 rounded transition-colors",
                ),
                rx.el.button(
                    rx.icon(
                        "copy",
                        size=16,
                        class_name="text-gray-400 hover:text-indigo-600",
                    ),
                    on_click=lambda: BudgetState.duplicate_expense(expense),
                    class_name="p-1 hover:bg-gray-100 rounded transition-colors",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2",
                        size=16,
                        class_name="text-gray-400 hover:text-red-600",
                    ),
                    on_click=lambda: BudgetState.delete_expense(expense["id"]),
                    class_name="p-1 hover:bg-gray-100 rounded transition-colors",
                ),
                class_name="flex gap-2",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name=rx.cond(
            BudgetState.selected_expense_ids.contains(expense["id"]),
            "bg-indigo-50/60 hover:bg-indigo-50 transition-colors border-b border-gray-100 last:border-0",
            "hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
        ),
    )


def bulk_actions_toolbar() -> rx.Component:
    return rx.cond(
        BudgetState.selected_expense_ids.length() > 0,
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"{BudgetState.selected_expense_ids.length()} selected",
                    class_name="text-sm font-semibold text-gray-700 bg-gray-100 px-3 py-1 rounded-full",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("check", size=16, class_name="mr-2"),
                        "Approve",
                        on_click=BudgetState.approve_selected_expenses,
                        class_name="flex items-center px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("x", size=16, class_name="mr-2"),
                        "Reject",
                        on_click=BudgetState.reject_selected_expenses,
                        class_name="flex items-center px-3 py-2 bg-white border border-gray-200 hover:bg-orange-50 hover:text-orange-600 text-gray-700 text-sm font-medium rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("download", size=16, class_name="mr-2"),
                        "Export",
                        on_click=BudgetState.export_selected_expenses,
                        class_name="flex items-center px-3 py-2 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-sm font-medium rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", size=16, class_name="mr-2"),
                        "Delete",
                        on_click=BudgetState.delete_selected_expenses,
                        class_name="flex items-center px-3 py-2 bg-white border border-gray-200 hover:bg-red-50 hover:text-red-600 text-gray-700 text-sm font-medium rounded-lg transition-colors",
                    ),
                    class_name="flex items-center gap-2 ml-4",
                ),
                class_name="flex items-center justify-between w-full",
            ),
            class_name="fixed bottom-8 left-1/2 -translate-x-1/2 bg-white p-4 rounded-xl shadow-lg border border-gray-200 flex items-center gap-4 z-40 animate-in slide-in-from-bottom-4 duration-300 min-w-[400px]",
        ),
    )


def fab_add_expense() -> rx.Component:
    return rx.el.button(
        rx.icon("plus", size=24, class_name="text-white"),
        on_click=BudgetState.open_add_expense_modal,
        class_name="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full shadow-lg shadow-indigo-300 flex items-center justify-center hover:scale-110 active:scale-95 transition-all duration-300 z-50 animate-bounce-in",
        title="Log New Expense",
    )


def expenses_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="fixed inset-0 bg-gradient-to-br from-indigo-50/50 via-purple-50/30 to-white -z-10"
        ),
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Expenses",
                                class_name="text-3xl font-bold text-gray-900 tracking-tight",
                            ),
                            rx.el.p(
                                "Track and approve team expenses.",
                                class_name="text-gray-500 mt-2 text-lg",
                            ),
                        ),
                        class_name="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-10",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search",
                                size=18,
                                class_name="text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                            ),
                            rx.el.input(
                                placeholder="Search expenses...",
                                on_change=BudgetState.set_expense_search,
                                class_name="pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-full sm:w-72 bg-gray-50/50 transition-all",
                                default_value=BudgetState.expense_search,
                            ),
                            class_name="relative",
                        ),
                        rx.el.select(
                            rx.el.option("All Categories", value="All"),
                            rx.foreach(
                                BudgetState.budgets,
                                lambda b: rx.el.option(b["name"], value=b["name"]),
                            ),
                            value=BudgetState.expense_category_filter,
                            on_change=BudgetState.set_expense_category_filter,
                            class_name="px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/50",
                        ),
                        class_name="flex flex-wrap gap-4 mb-6 bg-white/70 backdrop-blur-xl p-4 rounded-2xl border border-white/50 shadow-sm animate-in fade-in slide-in-from-bottom-4 duration-500",
                    ),
                    rx.el.div(
                        rx.cond(
                            BudgetState.filtered_expenses.length() > 0,
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                rx.el.input(
                                                    type="checkbox",
                                                    on_change=lambda _: BudgetState.toggle_all_expenses(),
                                                    checked=BudgetState.selected_expense_ids.length()
                                                    == BudgetState.filtered_expenses.length(),
                                                    class_name="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 h-4 w-4",
                                                ),
                                                class_name="px-6 py-4 text-left w-4",
                                            ),
                                            rx.el.th(
                                                "Date",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Category",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Description",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Amount",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Payment",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Status",
                                                class_name="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "", class_name="px-6 py-4 text-right"
                                            ),
                                            class_name="bg-gray-50/50 border-b border-gray-100",
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            BudgetState.filtered_expenses,
                                            expense_row_actions,
                                        ),
                                        class_name="bg-white/50 divide-y divide-gray-100",
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            empty_state(
                                icon="search-x",
                                title="No expenses found",
                                description="Try adjusting your search or filters to find what you're looking for.",
                            ),
                        ),
                        class_name="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700",
                    ),
                    expense_modal(),
                    attachment_preview_modal(),
                    fab_add_expense(),
                    bulk_actions_toolbar(),
                    class_name="max-w-7xl mx-auto relative z-10",
                ),
                class_name="flex-1 p-6 md:p-8 overflow-y-auto scroll-smooth",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-hidden",
        ),
        class_name="flex h-screen bg-gray-50 font-['Inter']",
    )