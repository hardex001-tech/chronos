from fastapi import APIRouter
from core.scheduler import scheduler

router = APIRouter(prefix="/api/shift", tags=["Shifts"])

@router.get("/status")
def get_shift_status():
    """Return the current shift phase, circadian energy, and 24-hour schedule."""
    return scheduler.get_shift_for_date()
