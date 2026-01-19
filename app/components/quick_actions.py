import reflex as rx
from app.states.budget_state import BudgetState
from app.states.settings_state import SettingsState


def action_button(
    label: str, icon: str, on_click: rx.event.EventType, color: str = "indigo"
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon,
                size=20,
                class_name=f"text-{color}-600 mb-2 group-hover:scale-110 transition-transform",
            ),
            rx.el.span(label, class_name="text-xs font-semibold text-gray-700"),
            class_name=f"flex flex-col items-center justify-center p-4 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 w-full h-full group",
        ),
        on_click=on_click,
        class_name="w-full",
    )


def quick_actions_panel() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Quick Actions", class_name="text-lg font-bold text-gray-900 mb-4"),
        rx.el.div(
            action_button(
                "New Expense", "receipt", BudgetState.open_add_expense_modal, "blue"
            ),
            action_button(
                "New Budget", "wallet", BudgetState.open_add_budget_modal, "emerald"
            ),
            action_button(
                "Export Report", "file-down", SettingsState.export_data, "purple"
            ),
            action_button("View Team", "users", rx.redirect("/team"), "orange"),
            class_name="grid grid-cols-2 sm:grid-cols-4 gap-4",
        ),
        class_name="mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700",
    )