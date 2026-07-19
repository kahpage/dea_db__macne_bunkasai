# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = list(range(1, 14 + 1))

    i = 1  # ==== macne_bunkasai1 ====
    if i in active_events:
        event_name = f"macne_bunkasai{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.4471499, 139.6432575),
                address="2 Yamashitacho, Naka Ward, Yokohama, Kanagawa 231-0023, Japan",
                description="横浜産貿ホール　マリネリア全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20110903030244/https://vocaloid-fantasia.com/about02.htm",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn3j0r7jhTBvDEmCgBnlhwXrSYHHrkl3fqXnrZDIY8cCVr146rAAv7f4-86On8aWyTCrywzJEL_vYeMyux_gNF4fW3166cMPmdL8k1ZZiWV5_1TOMRlOt6LiAbYpurFO0j4Gw06wg=w408-h272-k-no",
                url="https://maps.app.goo.gl/QB2yHxZahKtTi3Sk7",
            ),
        ]
        event = Event(
            aliases=["まくねけ文化祭", "Macne Bunkasai"],
            dates="2011.09.18",
            circles=[],
            media=media_,
            sources=[
                Source("Date: refer to VOCALOID Fantasia 2.", (RT.Reliable, OT.Official)),
                Source(
                    "Participating circles, same venue as VOCALOID Fantasia 2: https://web.archive.org/web/20110914172653/http://vocaloid-fantasia.com/cir02-iciran-k.htm",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            description="Simultaneous with VOCALOID Fantasia 2.",
            # comments=None,
            last_edited="2026.06.21",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    # ==== event group ====
    media = [
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        # "https://web.archive.org/web/20110914172653/http://vocaloid-fantasia.com/cir02-iciran-k.htm",
    ]

    event_group = EventGroup(
        aliases=["まくねけ文化祭", "Macne Bunkasai"],
        events=events,
        media=media,
        links=links,
        sources=[
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        comments="Only one event is known so far, but not much information is available.",
        description="Macne (Mac音)-themed event.",
        last_edited="2026.06.21",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
