"""Thin wrapper for simulation helpers used by the simulate route."""

from typing import Any, Dict, List, Optional


class SimulationService:
    """Minimal compatibility service for the simulate endpoint."""

    def simulate(self, profile: Optional[Dict[str, Any]] = None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "profile": profile or {},
            "overrides": overrides or {},
            "message": "Simulation completed.",
        }
