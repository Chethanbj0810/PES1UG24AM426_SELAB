"""Campus shuttle timetable, passenger-load, and fleet tracking tools."""

import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

MIN_CAPACITY = 10

routes: dict[str, dict[str, Any]] = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}


def _get_route(route_id: str) -> dict[str, Any]:
    """Return a route or raise a clear error when its ID is unknown."""
    if not isinstance(route_id, str) or route_id not in routes:
        expected_routes = ", ".join(routes)
        raise ValueError(
            f"Unknown route: {route_id}. Expected one of {expected_routes}."
        )
    return routes[route_id]


def add_trip_log(
    route_id: str,
    passenger_count: int,
    logs: list[str] | None = None,
) -> list[str]:
    """Record a non-negative integer passenger count for a known route."""
    route = _get_route(route_id)
    if (
        not isinstance(passenger_count, int)
        or isinstance(passenger_count, bool)
        or passenger_count < 0
    ):
        raise ValueError("Passenger count must be a non-negative integer.")

    if logs is None:
        logs = []
    elif (
        not isinstance(logs, list)
        or any(not isinstance(entry, str) for entry in logs)
    ):
        raise TypeError("Logs must be a list of strings.")

    route["trips"].append(passenger_count)
    timestamp = datetime.now().isoformat(timespec="seconds")
    logs.append(f"{timestamp}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id: str) -> None:
    """Remove a known route from the in-memory fleet."""
    _get_route(route_id)
    del routes[route_id]


def average_load(route_id: str) -> float:
    """Return the average passenger count, or zero when no trips are logged."""
    trips = _get_route(route_id)["trips"]
    if not trips:
        return 0.0
    return sum(trips) / len(trips)


def underused_routes() -> list[str]:
    """Return route IDs whose average load is below the minimum capacity."""
    return [
        route_id
        for route_id in routes
        if average_load(route_id) < MIN_CAPACITY
    ]


def assign_driver(route_id: str) -> str:
    """Choose a driver for a known route."""
    _get_route(route_id)
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return secrets.choice(drivers)


def sync_fleet_data(file: str | Path = "fleet.json") -> dict[str, Any]:
    """Save route data as UTF-8 JSON and return the saved representation."""
    if not isinstance(file, (str, Path)):
        raise TypeError(
            "Fleet data destination must be a string or pathlib.Path."
        )

    file_path = Path(file)
    with file_path.open("w", encoding="utf-8") as fleet_file:
        json.dump(routes, fleet_file, indent=2)

    with file_path.open("r", encoding="utf-8") as fleet_file:
        return json.load(fleet_file)


def main() -> None:
    """Run a small demonstration of the campus shuttle tracker."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    add_trip_log("R2", 6)
    add_trip_log("R3", 15)

    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))

    sync_fleet_data()

    choice = input("Route to look up (Enter for R2): ").strip() or "R2"
    if choice not in routes:
        print(f"Unknown route: {choice}")
        return

    print("Trips on", choice, ":", routes[choice]["trips"])
    print("R3 average:", average_load("R3"))


if __name__ == "__main__":
    main()
