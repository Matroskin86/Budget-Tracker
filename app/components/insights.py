import reflex as rx
from app.states.dashboard_state import DashboardState


def insight_item(text: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("sparkles", size=16, class_name="text-purple-600"),
            class_name="p-1.5 bg-purple-100 rounded-full mr-3 shrink-0",
        ),
        rx.el.p(text, class_name="text-sm text-gray-600 leading-snug"),
        class_name="flex items-start p-3 hover:bg-white/50 rounded-xl transition-colors",
    )


def insights_widget() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Smart Insights", class_name="text-lg font-bold text-gray-900"),
            rx.icon("brain-circuit", size=18, class_name="text-purple-500"),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.foreach(DashboardState.spending_insights, insight_item),
            class_name="space-y-1",
        ),
        class_name="bg-gradient-to-br from-white/80 to-purple-50/50 backdrop-blur-xl p-6 rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] h-full",
    )