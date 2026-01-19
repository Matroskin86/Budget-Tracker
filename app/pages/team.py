import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.empty_state import empty_state
from app.states.team_state import TeamState, TeamMember
from app.states.budget_state import BudgetState


def member_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Active",
            rx.el.span(
                "Active",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
            ),
        ),
        (
            "On Leave",
            rx.el.span(
                "On Leave",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
        ),
        (
            "Remote",
            rx.el.span(
                "Remote",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
        ),
        rx.el.span(
            status,
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def member_card(member: TeamMember) -> rx.Component:
    utilization = rx.cond(
        member["assigned_budget"] > 0,
        member["spent_amount"] / member["assigned_budget"] * 100,
        0,
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={member['avatar_seed']}",
                    class_name="w-16 h-16 rounded-full bg-gray-50 border-4 border-white shadow-sm",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("gallery_thumbnails", size=16),
                        class_name="text-gray-400 hover:text-gray-600 p-1",
                    ),
                    class_name="absolute top-4 right-4",
                ),
                class_name="flex justify-between items-start mb-4",
            ),
            rx.el.div(
                rx.el.h3(member["name"], class_name="text-lg font-bold text-gray-900"),
                rx.el.p(member["role"], class_name="text-sm text-gray-500 font-medium"),
                class_name="mb-3",
            ),
            rx.el.div(
                member_status_badge(member["status"]),
                rx.el.span(
                    member["department"],
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 ml-2",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Budget Usage",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.span(
                        f"{utilization:.0f}%",
                        class_name="text-xs font-bold text-gray-700",
                    ),
                    class_name="flex justify-between mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-2 rounded-full bg-indigo-500",
                        style={"width": f"{utilization}%"},
                    ),
                    class_name="w-full h-2 bg-gray-100 rounded-full overflow-hidden mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        f"${member['spent_amount']:,.0f} spent",
                        class_name="text-xs text-gray-500",
                    ),
                    rx.el.span(
                        f"${member['assigned_budget']:,.0f} limit",
                        class_name="text-xs text-gray-400",
                    ),
                    class_name="flex justify-between",
                ),
                class_name="mb-6 p-3 bg-gray-50 rounded-xl",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("mail", size=16, class_name="text-gray-500"),
                    href=f"mailto:{member['email']}",
                    class_name="p-2 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg transition-colors",
                ),
                rx.el.a(
                    rx.icon("phone", size=16, class_name="text-gray-500"),
                    href=f"tel:{member['phone']}",
                    class_name="p-2 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition-colors",
                ),
                rx.el.div(class_name="flex-1"),
                rx.el.button(
                    "Edit",
                    on_click=lambda: TeamState.open_edit_member_modal(member),
                    class_name="text-xs font-medium text-gray-600 hover:text-indigo-600 px-3 py-1.5 hover:bg-gray-100 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-2 pt-4 border-t border-gray-100",
            ),
            class_name="relative",
        ),
        class_name="bg-white/70 backdrop-blur-xl p-6 rounded-2xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 hover:-translate-y-1",
    )


def member_modal() -> rx.Component:
    return rx.cond(
        TeamState.is_member_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity",
                on_click=TeamState.close_member_modal,
            ),
            rx.el.div(
                rx.el.h3(
                    rx.cond(
                        TeamState.current_member["id"],
                        "Edit Team Member",
                        "Add Team Member",
                    ),
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Full Name",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                default_value=TeamState.current_member["name"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "name", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                                placeholder="e.g. John Doe",
                            ),
                            class_name="col-span-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Role",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                default_value=TeamState.current_member["role"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "role", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                                placeholder="e.g. Senior Analyst",
                            ),
                            class_name="col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Department",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    BudgetState.departments,
                                    lambda d: rx.el.option(d, value=d),
                                ),
                                value=TeamState.current_member["department"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "department", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                            ),
                            class_name="col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                default_value=TeamState.current_member["email"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "email", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                                type="email",
                                placeholder="john@company.com",
                            ),
                            class_name="col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Phone",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                default_value=TeamState.current_member["phone"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "phone", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                                placeholder="+1 (555) 000-0000",
                            ),
                            class_name="col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Assigned Budget",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                default_value=TeamState.current_member[
                                    "assigned_budget"
                                ],
                                on_change=lambda v: TeamState.update_current_member(
                                    "assigned_budget", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                                type="number",
                            ),
                            class_name="col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Status",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Active", value="Active"),
                                rx.el.option("On Leave", value="On Leave"),
                                rx.el.option("Remote", value="Remote"),
                                value=TeamState.current_member["status"],
                                on_change=lambda v: TeamState.update_current_member(
                                    "status", v
                                ),
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2 border",
                            ),
                            class_name="col-span-1",
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.cond(
                            TeamState.current_member["id"],
                            rx.el.button(
                                "Delete Member",
                                on_click=lambda: TeamState.delete_member(
                                    TeamState.current_member["id"]
                                ),
                                class_name="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors mr-auto",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                on_click=TeamState.close_member_modal,
                                class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-3",
                            ),
                            rx.el.button(
                                "Save Member",
                                on_click=TeamState.save_member,
                                class_name="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700",
                            ),
                            class_name="flex",
                        ),
                        class_name="flex justify-between items-center",
                    ),
                ),
                class_name="relative bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 z-50 animate-in fade-in zoom-in duration-200",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
        rx.el.div(),
    )


def fab_add_member() -> rx.Component:
    return rx.el.button(
        rx.icon("plus", size=24, class_name="text-white"),
        on_click=TeamState.open_add_member_modal,
        class_name="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full shadow-lg shadow-indigo-300 flex items-center justify-center hover:scale-110 active:scale-95 transition-all duration-300 z-50 animate-bounce-in",
        title="Add Team Member",
    )


def team_page() -> rx.Component:
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
                                "Team Members",
                                class_name="text-3xl font-bold text-gray-900 tracking-tight",
                            ),
                            rx.el.p(
                                "Manage team access, roles, and budget allocations.",
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
                                placeholder="Search members...",
                                on_change=TeamState.set_member_search,
                                class_name="pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-full sm:w-72 bg-gray-50/50 transition-all",
                                default_value=TeamState.member_search,
                            ),
                            class_name="relative",
                        ),
                        rx.el.select(
                            rx.el.option("All Departments", value="All"),
                            rx.foreach(
                                BudgetState.departments,
                                lambda d: rx.el.option(d, value=d),
                            ),
                            value=TeamState.department_filter,
                            on_change=TeamState.set_department_filter,
                            class_name="px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white/50",
                        ),
                        class_name="flex flex-wrap gap-4 mb-6 bg-white/70 backdrop-blur-xl p-4 rounded-2xl border border-white/50 shadow-sm animate-in fade-in slide-in-from-bottom-4 duration-500",
                    ),
                    rx.cond(
                        TeamState.filtered_members.length() > 0,
                        rx.el.div(
                            rx.foreach(TeamState.filtered_members, member_card),
                            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-6 duration-700",
                        ),
                        empty_state(
                            icon="users",
                            title="No team members found",
                            description="Try adjusting your search filters or add a new team member to get started.",
                            action_label="Add Team Member",
                            on_click=TeamState.open_add_member_modal,
                        ),
                    ),
                    member_modal(),
                    fab_add_member(),
                    class_name="max-w-7xl mx-auto relative z-10",
                ),
                class_name="flex-1 p-6 md:p-8 overflow-y-auto scroll-smooth",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-hidden",
        ),
        class_name="flex h-screen bg-gray-50 font-['Inter']",
    )