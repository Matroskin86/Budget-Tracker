import reflex as rx
from app.states.budget_state import BudgetState, BudgetStats


def budget_health_row(budget: BudgetStats) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                budget["name"],
                class_name="text-sm font-semibold text-gray-900 w-32 truncate",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=f"h-2 rounded-full {budget['progress_color']}",
                    style={"width": f"{budget['utilization']}%"},
                ),
                class_name="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden mx-3",
            ),
            rx.el.div(
                rx.el.span(
                    f"{budget['utilization']}%",
                    class_name="text-xs font-bold text-gray-700 w-10 text-right mr-3",
                ),
                rx.el.span(
                    rx.cond(
                        budget["utilization"] > 90,
                        "Critical",
                        rx.cond(budget["utilization"] > 75, "Warning", "Healthy"),
                    ),
                    class_name=f"text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full {budget['health_bg']} {budget['health_color']} w-20 text-center",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center",
        ),
        class_name="py-3 border-b border-gray-50 last:border-0 hover:bg-white/50 transition-colors px-2 rounded-lg",
    )


def budget_health_widget() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Budget Health Overview", class_name="text-lg font-bold text-gray-900"
            ),
            rx.el.a(
                "Manage",
                href="/budgets",
                class_name="text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.foreach(BudgetState.budget_stats, budget_health_row),
            class_name="flex flex-col max-h-[300px] overflow-y-auto custom-scrollbar pr-2",
        ),
        class_name="bg-white/70 backdrop-blur-xl p-6 rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] h-full",
    )