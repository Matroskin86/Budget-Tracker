import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stats import stats_grid
from app.components.charts import budget_chart
from app.components.expenses import expenses_table
from app.components.activity import activity_feed
from app.components.goals_widget import goals_widget
from app.components.budget_health import budget_health_widget
from app.components.quick_actions import quick_actions_panel
from app.components.alerts import alerts_panel
from app.components.insights import insights_widget
from app.pages.budgets import budget_modal
from app.pages.expenses import expense_modal


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Dashboard Overview", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Track your team's spending and budget health in real-time.",
                class_name="text-gray-600 mb-6",
            ),
            class_name="mb-6 animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        quick_actions_panel(),
        alerts_panel(),
        rx.el.div(
            stats_grid(),
            class_name="mb-8 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100",
        ),
        rx.el.div(
            rx.el.div(budget_chart(), class_name="lg:col-span-2"),
            rx.el.div(insights_widget(), class_name="lg:col-span-1"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200",
        ),
        rx.el.div(
            rx.el.div(budget_health_widget(), class_name="lg:col-span-2"),
            rx.el.div(activity_feed(), class_name="lg:col-span-1"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200",
        ),
        rx.el.div(
            rx.el.div(goals_widget(), class_name="lg:col-span-1"),
            rx.el.div(expenses_table(), class_name="lg:col-span-2"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 animate-in fade-in slide-in-from-bottom-9 duration-700 delay-250",
        ),
        budget_modal(),
        expense_modal(),
        class_name="max-w-7xl mx-auto relative z-10",
    )


def background_pattern() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute top-0 left-0 w-full h-96 bg-gradient-to-br from-indigo-100/40 via-purple-100/30 to-transparent -z-10"
        ),
        rx.el.div(
            class_name="absolute top-[-50px] right-[-50px] w-96 h-96 bg-purple-200/30 rounded-full blur-3xl -z-10 mix-blend-multiply filter opacity-70 animate-blob"
        ),
        rx.el.div(
            class_name="absolute top-[-50px] left-[-50px] w-96 h-96 bg-indigo-200/30 rounded-full blur-3xl -z-10 mix-blend-multiply filter opacity-70 animate-blob animation-delay-2000"
        ),
        class_name="fixed inset-0 overflow-hidden pointer-events-none",
    )


def index() -> rx.Component:
    return rx.el.div(
        background_pattern(),
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                dashboard_content(),
                class_name="flex-1 p-6 md:p-8 overflow-y-auto scroll-smooth",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-hidden bg-gray-50/30 backdrop-blur-sm",
        ),
        class_name="flex h-screen bg-gray-50 font-['Inter'] selection:bg-indigo-100 selection:text-indigo-900",
    )


from app.pages.budgets import budgets_page
from app.pages.expenses import expenses_page
from app.pages.reports import reports_page
from app.pages.settings import settings_page
from app.pages.team import team_page
from app.pages.goals import goals_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/")
app.add_page(budgets_page, route="/budgets")
app.add_page(expenses_page, route="/expenses")
app.add_page(team_page, route="/team")
app.add_page(goals_page, route="/goals")
app.add_page(reports_page, route="/reports")
app.add_page(settings_page, route="/settings")