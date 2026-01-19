import reflex as rx
from app.states.budget_state import BudgetState
from app.states.team_state import TeamState


class DashboardState(rx.State):
    """State for managing dashboard specific insights and alerts."""

    @rx.var
    async def budget_alerts(self) -> list[str]:
        """Returns a list of critical budget alerts."""
        bs = await self.get_state(BudgetState)
        alerts = []
        for b in bs.budgets:
            spent = sum(
                (
                    e["amount"]
                    for e in bs.expenses
                    if e["category"] == b["name"] and e["approval_status"] != "Rejected"
                )
            )
            total = b["allocated_amount"]
            if total > 0:
                utilization = spent / total * 100
                if utilization > bs.critical_threshold:
                    alerts.append(
                        f"Critical: {b['name']} is at {utilization:.1f}% utilization"
                    )
                elif utilization > bs.warning_threshold:
                    alerts.append(
                        f"Warning: {b['name']} is at {utilization:.1f}% utilization"
                    )
        return alerts

    @rx.var
    async def spending_insights(self) -> list[str]:
        """Returns AI-like spending recommendations."""
        bs = await self.get_state(BudgetState)
        insights = []
        if bs.total_spent > bs.total_budget * 0.8:
            insights.append(
                "Spending velocity is high. Consider freezing non-essential expenses."
            )
        pending_count = len(
            [e for e in bs.expenses if e["approval_status"] == "Pending"]
        )
        if pending_count > 5:
            insights.append(
                f"You have {pending_count} pending approvals. Clearing these will update accurate spend data."
            )
        if bs.category_distribution:
            top_cat = max(bs.category_distribution, key=lambda x: x["value"])
            insights.append(
                f"{top_cat['name']} accounts for the largest share of expenses. Review mainly recurring costs there."
            )
        if not insights:
            insights.append("Budget health looks good. Keep tracking expenses daily.")
        return insights