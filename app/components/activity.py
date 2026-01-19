import reflex as rx
from app.states.team_state import TeamState, Activity


def activity_icon(type_str: str) -> rx.Component:
    return rx.match(
        type_str,
        (
            "expense",
            rx.el.div(
                rx.icon("receipt", size=16, class_name="text-blue-600"),
                class_name="bg-blue-100 p-2 rounded-full",
            ),
        ),
        (
            "budget",
            rx.el.div(
                rx.icon("wallet", size=16, class_name="text-emerald-600"),
                class_name="bg-emerald-100 p-2 rounded-full",
            ),
        ),
        (
            "warning",
            rx.el.div(
                rx.icon("trending_down", size=16, class_name="text-orange-600"),
                class_name="bg-orange-100 p-2 rounded-full",
            ),
        ),
        rx.el.div(
            rx.icon("info", size=16, class_name="text-gray-600"),
            class_name="bg-gray-100 p-2 rounded-full",
        ),
    )


def activity_item(activity: Activity) -> rx.Component:
    return rx.el.div(
        rx.el.div(activity_icon(activity["type"]), class_name="mr-4 relative z-10"),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    activity["user_name"], class_name="font-semibold text-gray-900 mr-1"
                ),
                rx.el.span(activity["action"], class_name="text-gray-600 mr-1"),
                rx.el.span(activity["target"], class_name="font-medium text-gray-900"),
                class_name="text-sm",
            ),
            rx.el.span(
                activity["timestamp"], class_name="text-xs text-gray-400 mt-0.5 block"
            ),
            class_name="flex-1 py-1",
        ),
        class_name="flex items-start mb-6 last:mb-0 relative before:content-[''] before:absolute before:left-[19px] before:top-8 before:bottom-[-24px] before:w-[2px] before:bg-gray-100 last:before:hidden",
    )


def activity_feed() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Recent Activity", class_name="text-lg font-bold text-gray-900"),
            rx.el.select(
                rx.el.option("All", value="All"),
                rx.el.option("Expenses", value="Expense"),
                rx.el.option("Budgets", value="Budget"),
                rx.el.option("System", value="System"),
                rx.el.option("Warnings", value="Warning"),
                value=TeamState.activity_filter,
                on_change=TeamState.set_activity_filter,
                class_name="text-xs font-medium text-gray-600 bg-gray-50 border-none rounded-lg focus:ring-1 focus:ring-indigo-500 py-1 pl-2 pr-8 cursor-pointer hover:bg-gray-100 transition-colors",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.foreach(TeamState.filtered_activities, activity_item),
            class_name="max-h-[400px] overflow-y-auto pr-2 custom-scrollbar",
        ),
        class_name="bg-white/70 backdrop-blur-xl p-6 rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] h-full",
    )