from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
    responses={404: {"description": "Not found"}},
)

# Sample timeline data - TODO make a table out of this & replace with actual database operations
timeline_data = {
    "DC": [
        {
            "id": 1,
            "title": "Pre-Crisis",
            "ending event": "Crisis on Infinite Earths", 
            "years": [1938, 1985],
            "description": "Beginning of DC Comics up to the beginning of the modern age",
        },
        {
            "id": 2,
            "title": "Post-Crisis Part 1",
            "ending event": "Zero Hour", 
            "years": [1985, 1994],
            "description": "Modern age following Crisis on Infinite Earths through Zero Hour",
        },
        {
            "id": 3,
            "title": "Post-Crisis Part 2",
            "ending event": "Infinite Crisis",
            "years": [1994, 2005],
            "description": "DC expands as much as they can in a single continuity before another big event retconning everything",
        },
        {
            "id": 4,
            "title": "Post-Crisis Part 3",
            "ending event": "Final Crisis",
            "years": [2005, 2009],
            "description": "The newly streamlined continuity builds up to its most complicated event so far",
        },
        {
            "id": 5,
            "title": "Post-Crisis Part 4",
            "ending event": "Flashpoint",
            "years": [2009, 2011],
            "description": "Final chapter of the Post-Crisis era before the New 52",
        },
        {
            "id": 6,
            "title": "New 52",
            "years": [2011, 2016],
            "description": "DC Universe reboot following Flashpoint event",
        },
        {
            "id": 4,
            "title": "Rebirth",
            "years": [2016, 2024],
            "description": "Soft reboot bringing back classic elements to DC continuity",
        }
    ],
    "Marvel": [
        {
            "id": 5,
            "title": "Golden Age",
            "years": [1939, 1956],
            "description": "Early Marvel Comics under Timely Publications",
        },
        {
            "id": 6,
            "title": "Silver Age",
            "years": [1961, 1970],
            "description": "Marvel renaissance under Stan Lee",
        }
    ]
}

@router.get("/eras")
async def get_eras(
    publisher: Optional[str] = Query(None, description="Filter by publisher (DC, Marvel, etc.)"),
    start_year: Optional[int] = Query(None, description="Filter eras that start after this year"),
    end_year: Optional[int] = Query(None, description="Filter eras that end before this year")
) -> List[Dict[str, Any]]:
    """Get timeline eras with optional filtering"""
    
    # Start with all eras
    all_eras = []
    for pub, eras in timeline_data.items():
        if publisher is None or pub.lower() == publisher.lower():
            all_eras.extend(eras)
    
    # Apply year filters
    if start_year is not None:
        all_eras = [era for era in all_eras if era["years"][0] >= start_year]
    
    if end_year is not None:
        all_eras = [era for era in all_eras if era["years"][1] <= end_year]
    
    if not all_eras:
        raise HTTPException(status_code=404, detail="No eras found matching the criteria")
    
    return all_eras

@router.get("/eras/{era_id}")
async def get_era_details(era_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific era"""
    for eras in timeline_data.values():
        for era in eras:
            if era["id"] == era_id:
                return era
    raise HTTPException(status_code=404, detail="Era not found")

@router.get("/events")
async def get_major_events(
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    era_id: Optional[int] = Query(None, description="Filter by specific era"),
    year: Optional[int] = Query(None, description="Filter by specific year")
) -> List[Dict[str, Any]]:
    """Get major timeline events with optional filtering"""
    
    events = []
    
    for pub, eras in timeline_data.items():
        if publisher is None or pub.lower() == publisher.lower():
            for era in eras:
                if era_id is None or era["id"] == era_id:
                    for event in era["major_events"]:
                        if year is None or event["year"] == year:
                            events.append({
                                **event,
                                "era_title": era["title"],
                                "era_id": era["id"],
                                "publisher": pub
                            })
    
    if not events:
        raise HTTPException(status_code=404, detail="No events found matching the criteria")
    
    return sorted(events, key=lambda x: x["year"])

@router.get("/publishers")
async def get_publishers() -> List[Dict[str, Any]]:
    """Get all available publishers and their era counts"""
    publishers = []
    
    for pub, eras in timeline_data.items():
        publishers.append({
            "name": pub,
            "era_count": len(eras),
            "total_years": max(era["years"][1] for era in eras) - min(era["years"][0] for era in eras),
            "earliest_year": min(era["years"][0] for era in eras),
            "latest_year": max(era["years"][1] for era in eras)
        })
    
    return publishers

@router.get("/timeline/full")
async def get_full_timeline(
    publisher: Optional[str] = Query(None, description="Filter by publisher")
) -> Dict[str, Any]:
    """Get complete timeline data for visualization"""
    
    if publisher:
        if publisher not in timeline_data:
            raise HTTPException(status_code=404, detail=f"Publisher '{publisher}' not found")
        
        eras = timeline_data[publisher]
        return {
            "publisher": publisher,
            "eras": eras,
            "total_years": max(era["years"][1] for era in eras) - min(era["years"][0] for era in eras),
            "era_count": len(eras)
        }
    
    # Return all publishers' data
    return {
        "publishers": list(timeline_data.keys()),
        "all_data": timeline_data,
        "summary": {
            pub: {
                "era_count": len(eras),
                "year_span": f"{min(era['years'][0] for era in eras)}-{max(era['years'][1] for era in eras)}"
            }
            for pub, eras in timeline_data.items()
        }
    }

@router.get("/search")
async def search_timeline(
    query: str = Query(..., description="Search term for events, eras, or descriptions"),
    publisher: Optional[str] = Query(None, description="Filter by publisher")
) -> Dict[str, Any]:
    """Search through timeline data"""
    
    results = {
        "eras": [],
        "events": [],
        "query": query
    }
    
    query_lower = query.lower()
    
    for pub, eras in timeline_data.items():
        if publisher is None or pub.lower() == publisher.lower():
            for era in eras:
                # Search in era data
                if (query_lower in era["title"].lower() or 
                    query_lower in era["description"].lower()):
                    results["eras"].append({**era, "publisher": pub})
                
                # Search in events
                for event in era["major_events"]:
                    if (query_lower in event["name"].lower() or 
                        query_lower in event["description"].lower()):
                        results["events"].append({
                            **event,
                            "era_title": era["title"],
                            "era_id": era["id"],
                            "publisher": pub
                        })
    
    if not results["eras"] and not results["events"]:
        raise HTTPException(status_code=404, detail=f"No results found for query: {query}")
    
    return results
