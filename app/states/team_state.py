import reflex as rx
from typing import TypedDict
import datetime
import uuid
import random
import logging


class TeamMember(TypedDict):
    id: str
    name: str
    role: str
    department: str
    avatar_seed: str
    email: str
    phone: str
    status: str
    joined_date: str
    assigned_budget: float
    spent_amount: float


class Activity(TypedDict):
    id: str
    user_name: str
    user_avatar: str
    action: str
    target: str
    timestamp: str
    type: str


class TeamState(rx.State):
    """State for team management and activity tracking."""

    is_member_modal_open: bool = False
    member_search: str = ""
    department_filter: str = "All"
    activity_filter: str = "All"
    current_member: TeamMember = {
        "id": "",
        "name": "",
        "role": "",
        "department": "Marketing",
        "avatar_seed": "",
        "email": "",
        "phone": "",
        "status": "Active",
        "joined_date": "",
        "assigned_budget": 0.0,
        "spent_amount": 0.0,
    }
    team_members: list[TeamMember] = [
        {
            "id": "t1",
            "name": "Alex Finance",
            "role": "Admin",
            "department": "Finance",
            "avatar_seed": "Felix",
            "email": "alex@company.com",
            "phone": "+1 (555) 0101",
            "status": "Active",
            "joined_date": "2023-01-15",
            "assigned_budget": 0.0,
            "spent_amount": 0.0,
        },
        {
            "id": "t2",
            "name": "Sarah Marketing",
            "role": "Department Head",
            "department": "Marketing",
            "avatar_seed": "Sarah",
            "email": "sarah@company.com",
            "phone": "+1 (555) 0102",
            "status": "Active",
            "joined_date": "2023-02-01",
            "assigned_budget": 50000.0,
            "spent_amount": 35420.5,
        },
        {
            "id": "t3",
            "name": "Mike Engineering",
            "role": "CTO",
            "department": "Engineering",
            "avatar_seed": "Mike",
            "email": "mike@company.com",
            "phone": "+1 (555) 0103",
            "status": "Active",
            "joined_date": "2023-01-10",
            "assigned_budget": 120000.0,
            "spent_amount": 98500.0,
        },
        {
            "id": "t4",
            "name": "Jessica HR",
            "role": "HR Manager",
            "department": "HR",
            "avatar_seed": "Jessica",
            "email": "jessica@company.com",
            "phone": "+1 (555) 0104",
            "status": "Remote",
            "joined_date": "2023-03-15",
            "assigned_budget": 30000.0,
            "spent_amount": 12500.0,
        },
        {
            "id": "t5",
            "name": "David Sales",
            "role": "VP of Sales",
            "department": "Sales",
            "avatar_seed": "David",
            "email": "david@company.com",
            "phone": "+1 (555) 0105",
            "status": "On Leave",
            "joined_date": "2023-04-01",
            "assigned_budget": 80000.0,
            "spent_amount": 65000.0,
        },
        {
            "id": "t6",
            "name": "Emily Ops",
            "role": "Operations Manager",
            "department": "Operations",
            "avatar_seed": "Emily",
            "email": "emily@company.com",
            "phone": "+1 (555) 0106",
            "status": "Active",
            "joined_date": "2023-05-12",
            "assigned_budget": 45000.0,
            "spent_amount": 28900.0,
        },
    ]
    activities: list[Activity] = [
        {
            "id": "a1",
            "user_name": "Sarah Marketing",
            "user_avatar": "Sarah",
            "action": "approved expense",
            "target": "Q2 Media Buy ($8,000)",
            "timestamp": "2 hours ago",
            "type": "expense",
        },
        {
            "id": "a2",
            "user_name": "Mike Engineering",
            "user_avatar": "Mike",
            "action": "created budget",
            "target": "AI Research Project",
            "timestamp": "5 hours ago",
            "type": "budget",
        },
        {
            "id": "a3",
            "user_name": "Alex Finance",
            "user_avatar": "Felix",
            "action": "updated settings",
            "target": "Global Currency Format",
            "timestamp": "1 day ago",
            "type": "system",
        },
        {
            "id": "a4",
            "user_name": "Jessica HR",
            "user_avatar": "Jessica",
            "action": "added member",
            "target": "Tom Intern",
            "timestamp": "1 day ago",
            "type": "system",
        },
        {
            "id": "a5",
            "user_name": "David Sales",
            "user_avatar": "David",
            "action": "exceeded budget",
            "target": "Travel Q1",
            "timestamp": "2 days ago",
            "type": "warning",
        },
    ]

    @rx.var
    def filtered_members(self) -> list[TeamMember]:
        members = self.team_members
        if self.department_filter != "All":
            members = [m for m in members if m["department"] == self.department_filter]
        if self.member_search:
            search = self.member_search.lower()
            members = [
                m
                for m in members
                if search in m["name"].lower() or search in m["role"].lower()
            ]
        return sorted(members, key=lambda x: x["name"])

    @rx.var
    def filtered_activities(self) -> list[Activity]:
        if self.activity_filter == "All":
            return self.activities
        filter_map = {
            "Expense": "expense",
            "Budget": "budget",
            "System": "system",
            "Warning": "warning",
        }
        target_type = filter_map.get(self.activity_filter, self.activity_filter.lower())
        return [a for a in self.activities if a["type"] == target_type]

    @rx.var
    def top_spenders(self) -> list[TeamMember]:
        return sorted(self.team_members, key=lambda x: x["spent_amount"], reverse=True)[
            :5
        ]

    @rx.event
    def set_member_search(self, value: str):
        self.member_search = value

    @rx.event
    def set_activity_filter(self, value: str):
        self.activity_filter = value

    @rx.event
    def set_department_filter(self, value: str):
        self.department_filter = value

    @rx.event
    def open_add_member_modal(self):
        self.current_member = {
            "id": "",
            "name": "",
            "role": "",
            "department": "Marketing",
            "avatar_seed": str(random.randint(1000, 9999)),
            "email": "",
            "phone": "",
            "status": "Active",
            "joined_date": datetime.date.today().isoformat(),
            "assigned_budget": 0.0,
            "spent_amount": 0.0,
        }
        self.is_member_modal_open = True

    @rx.event
    def open_edit_member_modal(self, member: TeamMember):
        self.current_member = member
        self.is_member_modal_open = True

    @rx.event
    def close_member_modal(self):
        self.is_member_modal_open = False

    @rx.event
    def update_current_member(self, key: str, value: str):
        if key in ["assigned_budget", "spent_amount"]:
            try:
                self.current_member[key] = float(value)
            except ValueError as e:
                logging.exception(f"Error updating member {key}: {e}")
        else:
            self.current_member[key] = value

    @rx.event
    def save_member(self):
        if not self.current_member["name"]:
            return
        if self.current_member["id"]:
            self.team_members = [
                m if m["id"] != self.current_member["id"] else self.current_member
                for m in self.team_members
            ]
            self.add_activity(f"updated profile", self.current_member["name"], "system")
        else:
            new_member = self.current_member.copy()
            new_member["id"] = str(uuid.uuid4())
            if not new_member["avatar_seed"]:
                new_member["avatar_seed"] = new_member["name"]
            self.team_members.append(new_member)
            self.add_activity(f"joined the team", self.current_member["name"], "system")
        self.close_member_modal()

    @rx.event
    def delete_member(self, id: str):
        member = next((m for m in self.team_members if m["id"] == id), None)
        if member:
            self.team_members = [m for m in self.team_members if m["id"] != id]
            self.add_activity(f"removed member", member["name"], "system")

    @rx.event
    def add_activity(self, action: str, target: str, type_str: str):
        new_activity: Activity = {
            "id": str(uuid.uuid4()),
            "user_name": "Alex Finance",
            "user_avatar": "Felix",
            "action": action,
            "target": target,
            "timestamp": "Just now",
            "type": type_str,
        }
        self.activities.insert(0, new_activity)