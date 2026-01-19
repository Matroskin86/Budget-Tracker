import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.budget_state import BudgetState


def alert_item(message: str) -> rx.Component:
    is_critical = message.startswith("Critical")
    return rx.el.div(
        rx.icon(
            rx.cond(is_critical, "alert-triangle", "alert-circle"),
            size=18,
            class_name=rx.cond(is_critical, "text-red-500", "text-orange-500"),
        ),
        rx.el.span(message, class_name="text-sm text-gray-700 font-medium ml-3"),
        class_name=rx.cond(
            is_critical,
            "flex items-center p-3 bg-red-50 rounded-lg border border-red-100",
            "flex items-center p-3 bg-orange-50 rounded-lg border border-orange-100",
        ),
    )


def alerts_panel() -> rx.Component:
    return rx.cond(
        (DashboardState.budget_alerts.length() > 0)
        | (BudgetState.pending_approvals_count > 0),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Alerts & Attention", class_name="text-lg font-bold text-gray-900"
                ),
                rx.cond(
                    BudgetState.pending_approvals_count > 0,
                    rx.el.span(
                        f"{BudgetState.pending_approvals_count} Pending Approvals",
                        class_name="text-xs font-bold text-white bg-indigo-500 px-2 py-1 rounded-full animate-pulse",
                    ),
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.div(
                rx.foreach(DashboardState.budget_alerts, alert_item),
                rx.cond(
                    BudgetState.pending_approvals_count > 0,
                    rx.el.a(
                        rx.el.div(
                            rx.icon("clock", size=18, class_name="text-indigo-500"),
                            rx.el.span(
                                f"You have {BudgetState.pending_approvals_count} expenses waiting for approval",
                                class_name="text-sm text-gray-700 font-medium ml-3",
                            ),
                            class_name="flex items-center p-3 bg-indigo-50 rounded-lg border border-indigo-100 hover:bg-indigo-100 transition-colors",
                        ),
                        href="/expenses",
                        class_name="block",
                    ),
                ),
                class_name="space-y-3",
            ),
            class_name="bg-white/70 backdrop-blur-xl p-6 rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] mb-8 animate-in fade-in slide-in-from-bottom-5 duration-700",
        ),
    )