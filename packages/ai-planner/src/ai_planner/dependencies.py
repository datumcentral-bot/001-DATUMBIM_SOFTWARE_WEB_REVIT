from __future__ import annotations

from ai_planner.exceptions import DependencyError
from ai_planner.models import ActionPlan


class DependencyResolver:
    def resolve(self, plan: ActionPlan) -> ActionPlan:
        graph: dict[str, list[str]] = {}
        for action in plan.actions:
            graph[action.action_id] = list(action.dependencies)
        self._check_cycles(graph)
        ordered = self._topological_sort(graph)
        action_map = {action.action_id: action for action in plan.actions}
        ordered_actions = [action_map[aid] for aid in ordered if aid in action_map]
        plan.actions = ordered_actions
        plan.dependencies = graph
        return plan

    def _check_cycles(self, graph: dict[str, list[str]]) -> None:
        visited = set()
        rec_stack = set()
        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    raise DependencyError(f"Cycle detected involving {neighbor}")
            rec_stack.remove(node)
        for node in graph:
            if node not in visited:
                dfs(node)

    def _topological_sort(self, graph: dict[str, list[str]]) -> list[str]:
        reverse_graph: dict[str, list[str]] = {node: [] for node in graph}
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for dep in graph[node]:
                reverse_graph.setdefault(dep, []).append(node)
                in_degree[node] = in_degree.get(node, 0) + 1
        queue = [node for node in graph if in_degree[node] == 0]
        result = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in reverse_graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result
