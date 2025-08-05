from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
    responses={404: {"description": "Not found"}},
)

# Sample era data - TODO make a table out of this & replace with actual database operations
era_data = {
    "DC": [
        {
            "id": 1,
            "title": "Pre-Crisis",
            "ending_event": "Crisis on Infinite Earths", 
            "years": [1938, 1985],
            "description": "Beginning of DC Comics up to the beginning of the modern age",
        },
        {
            "id": 2,
            "title": "Post-Crisis Part 1",
            "ending_event": "Zero Hour", 
            "years": [1985, 1994],
            "description": "Modern age following Crisis on Infinite Earths through Zero Hour",
        },
        {
            "id": 3,
            "title": "Post-Crisis Part 2",
            "ending_event": "Infinite Crisis",
            "years": [1994, 2005],
            "description": "DC expands as much as they can in a single continuity before another big event retconning everything",
        },
        {
            "id": 4,
            "title": "Post-Crisis Part 3",
            "ending_event": "Final Crisis",
            "years": [2005, 2009],
            "description": "The newly streamlined continuity builds up to its most complicated event so far",
        },
        {
            "id": 5,
            "title": "Post-Crisis Part 4",
            "ending_event": "Flashpoint",
            "years": [2009, 2011],
            "description": "Final chapter of the Post-Crisis era before the New 52",
        },
        {
            "id": 6,
            "title": "New 52",
            "years": [2011, 2016],
            "ending_event": "Rebirth",
            "description": "DC Universe reboot following Flashpoint event",
        },
        {
            "id": 7,
            "title": "Rebirth",
            "years": [2016, 2018],
            "ending_event": "Doomsday Clock",
            "description": "Soft reboot bringing back classic elements to DC continuity",
        }
    ],
    "Marvel": [
        {
            "id": 8,
            "title": "Golden Age",
            "years": [1939, 1956],
            "description": "Early Marvel Comics under Timely Publications",
            "ending_event": "Creation of the Fantastic Four",
        },
        {
            "id": 9,
            "title": "The Marvel Age",
            "years": [1961, 1984],
            "description": "Marvel renaissance under Stan Lee(but also Jack Kirby, Steve Ditko, etc.)",
            "ending_event": "Secret Wars (1984)",
        },
        {
            "id": 10,
            "title": "Copper Age",
            "years": [1984, 1996],
            "description": "Marvel's response to the DC Crisis events, leading to a more interconnected universe",
            "ending_event": "Onslaught",
        },
        {
            "id": 11,
            "title": "Modern Age",
            "years": [1996, 2015],
            "description": "Marvel's current era with multiple reboots and continuities",
            "ending_event": "Secret Wars (2015)",
        },
        {
            "id": 12,
            "title": "All-New, All-Different Marvel",
            "years": [2015, 2025],
            "description": "Post-Secret Wars era with new directions for characters and teams",
            "ending_event": "Ongoing",
        }
    ]
}

# Sample subera data - TODO make a table out of this & replace with actual database operations

subera_data = {
    "DC": {
        "Pre-Crisis": [
            {}
        ],
        "Post-Crisis Part 1": [
            {} 
        ],
        "Post-Crisis Part 2": [
            {} 
        ],
        "Post-Crisis Part 3": [
            {} 
        ],
        "Post-Crisis Part 4": [
            {} 
        ],
        "New 52": [
            {} 
        ],
        "Rebirth": [
            {} 
        ],
    },
    "Marvel": {
        "Golden Age": [
            {}
        ],
        "The Marvel Age": [
            {}
        ],
        "Copper Age": [
            {}
        ],
        "Modern Age": [
            {}
        ]

    }

}

@router.get("/eras")
async def get_eras(
    publisher: Optional[str] = Query(None, description="Filter by publisher (DC, Marvel, etc.)"),
    start_year: Optional[int] = Query(None, description="Filter eras that start after this year"),
    end_year: Optional[int] = Query(None, description="Filter eras that end before this year")
) -> List[Dict[str, Any]]:
    all_eras = []
    for pub, eras in era_data.items():
        if publisher is None or pub.lower() == publisher.lower():
            all_eras.extend(eras)

    if start_year is not None:
        all_eras = [era for era in all_eras if era["years"][0] >= start_year]    
    if end_year is not None:
        all_eras = [era for era in all_eras if era["years"][1] <= end_year]
    if not all_eras:
        raise HTTPException(status_code=404, detail="No eras found matching the criteria")
    return all_eras

@router.get("/suberas")
async def get_suberas(
    publisher: str = Query(None, description="Filter by publisher (DC, Marvel, etc.)"),
    era_name: str = Query(None, description="Filter by specific era name")
) -> List[Dict[str, Any]]:
    return subera_data.get(publisher, {}).get(era_name, [])


# TODO IMPLEMENT SIMILAR LOGIC IN THE FUTURE 
# @router.get("/events")
# async def get_major_events(
#     publisher: Optional[str] = Query(None, description="Filter by publisher"),
#     era_id: Optional[int] = Query(None, description="Filter by specific era"),
#     year: Optional[int] = Query(None, description="Filter by specific year")
# ) -> List[Dict[str, Any]]:
#     """Get major timeline events with optional filtering"""
    
#     events = []
    
#     for pub, eras in timeline_data.items():
#         if publisher is None or pub.lower() == publisher.lower():
#             for era in eras:
#                 if era_id is None or era["id"] == era_id:
#                     for event in era["major_events"]:
#                         if year is None or event["year"] == year:
#                             events.append({
#                                 **event,
#                                 "era_title": era["title"],
#                                 "era_id": era["id"],
#                                 "publisher": pub
#                             })
    
#     if not events:
#         raise HTTPException(status_code=404, detail="No events found matching the criteria")
    
#     return sorted(events, key=lambda x: x["year"])


# @router.get("/timeline/full")
# async def get_full_timeline(
#     publisher: Optional[str] = Query(None, description="Filter by publisher")
# ) -> Dict[str, Any]:
#     """Get complete timeline data for visualization"""
    
#     if publisher:
#         if publisher not in timeline_data:
#             raise HTTPException(status_code=404, detail=f"Publisher '{publisher}' not found")
        
#         eras = timeline_data[publisher]
#         return {
#             "publisher": publisher,
#             "eras": eras,
#             "total_years": max(era["years"][1] for era in eras) - min(era["years"][0] for era in eras),
#             "era_count": len(eras)
#         }
    
#     # Return all publishers' data
#     return {
#         "publishers": list(timeline_data.keys()),
#         "all_data": timeline_data,
#         "summary": {
#             pub: {
#                 "era_count": len(eras),
#                 "year_span": f"{min(era['years'][0] for era in eras)}-{max(era['years'][1] for era in eras)}"
#             }
#             for pub, eras in timeline_data.items()
#         }
#     }
