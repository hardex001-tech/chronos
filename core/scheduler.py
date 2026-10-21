from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from config.settings import settings

class ShiftScheduler:
    def __init__(self, anchor_date: date = None, cycle_days: int = 9):
        self.anchor_date = anchor_date or settings.SHIFT_ANCHOR_DATE
        self.cycle_days = cycle_days

    def get_shift_for_date(self, target_date: date = None) -> Dict[str, Any]:
        """
        Calculate shift details for a given date.
        Cycle pattern (9 days total):
          - Days 0, 1, 2: Morning Shift (Day 1, 2, 3)
          - Days 3, 4, 5: Night Shift (Day 1, 2, 3)
          - Days 6, 7, 8: Power Off-Day (Day 1, 2, 3)
        """
        target = target_date or date.today()
        delta_days = (target - self.anchor_date).days
        cycle_day_idx = delta_days % self.cycle_days  # 0 to 8

        if 0 <= cycle_day_idx <= 2:
            shift_type = "Morning"
            sub_day = cycle_day_idx + 1  # 1, 2, or 3
            badge_color = "#3B82F6"  # Blue
            icon = "🌅"
            energy_level = "12h Shift Day"
            energy_desc = "12-Hour Shift (07:00 AM - 07:00 PM). Work duties & ad-hoc micro-breaks. Optional 30m evening review only if fresh. Sleep early."
            next_phase_name = "Night Shift"
            days_to_next = 3 - cycle_day_idx
        elif 3 <= cycle_day_idx <= 5:
            shift_type = "Night"
            sub_day = cycle_day_idx - 2  # 1, 2, or 3
            badge_color = "#8B5CF6"  # Purple
            icon = "🌙"
            energy_level = "12h Night Shift"
            energy_desc = "12-Hour Night Shift (07:00 PM - 07:00 AM). Inverted cycle. Mandatory daytime recovery sleep (08:00 AM - 03:30 PM). Zero forced study."
            next_phase_name = "Power Off-Days"
            days_to_next = 6 - cycle_day_idx
        else:
            shift_type = "Off"
            sub_day = cycle_day_idx - 5  # 1, 2, or 3
            badge_color = "#10B981"  # Emerald Green
            icon = "⚡"
            energy_level = "Maximum Power (Off-Day)"
            energy_desc = "Full Off-Day (Zero work shifts). High cognitive energy. 2 deep work power sprints for labs, lecture notes & building."
            next_phase_name = "Morning Shift"
            days_to_next = 9 - cycle_day_idx

        return {
            "target_date": target.isoformat(),
            "target_date_human": target.strftime("%A, %B %d, %Y"),
            "cycle_day_index": cycle_day_idx + 1,
            "shift_type": shift_type,
            "sub_day": sub_day,
            "shift_title": f"{icon} {shift_type} Shift (Day {sub_day} of 3)",
            "badge_color": badge_color,
            "energy_level": energy_level,
            "energy_desc": energy_desc,
            "next_phase": f"{next_phase_name} in {days_to_next} day(s)",
            "daily_plan": self._generate_24h_plan(shift_type, sub_day)
        }

    def _generate_24h_plan(self, shift_type: str, sub_day: int) -> List[Dict[str, str]]:
        """Generate tailored 24-hour itinerary matching 12-hour rotational shifts with explicit AM/PM."""
        if shift_type == "Morning":
            return [
                {"time": "05:45 AM - 07:00 AM", "activity": "Wake-up, Prep & Commute to Morning Shift", "category": "Routine"},
                {"time": "07:00 AM - 07:00 PM", "activity": "12-Hour Morning Shift (Work duties • Ad-hoc micro-reading if quiet)", "category": "Work (12h)"},
                {"time": "07:00 PM - 08:15 PM", "activity": "Commute from Work, Dinner & Decompress", "category": "Rest"},
                {"time": "08:30 PM - 09:15 PM", "activity": "Optional Evening Pocket (30-45m: FUNAAB notes or 1 Cloud lesson if energy allows)", "category": "Light Study"},
                {"time": "09:30 PM - 05:45 AM", "activity": "Mandatory Sleep & Recovery (Protect your body)", "category": "Sleep"}
            ]
        elif shift_type == "Night":
            return [
                {"time": "07:00 AM - 08:00 AM", "activity": "Return Home from Night Shift, Shower & Wind Down", "category": "Rest"},
                {"time": "08:00 AM - 03:30 PM", "activity": "Protected Daytime Recovery Sleep (7.5h uninterrupted • Do not disturb)", "category": "Sleep"},
                {"time": "03:30 PM - 05:00 PM", "activity": "Wake-up, Balanced Meal, Hydrate & Fresh Air", "category": "Health"},
                {"time": "05:00 PM - 06:15 PM", "activity": "Pre-Shift Reset • Optional: 1 OSINT/Cyber podcast or school notes", "category": "Light"},
                {"time": "06:15 PM - 07:00 PM", "activity": "Commute to Night Shift Station", "category": "Commute"},
                {"time": "07:00 PM - 07:00 AM", "activity": "12-Hour Night Shift (Work duties • Ad-hoc micro-reading if quiet)", "category": "Work (12h)"}
            ]
        else:  # Off days
            return [
                {"time": "08:00 AM - 09:30 AM", "activity": "Natural Wake-Up, Breakfast & Day Planning", "category": "Health"},
                {"time": "10:00 AM - 12:30 PM", "activity": "⚡ Power Engine Sprint 1: Hands-on Labs (Google Cloud / AWS / TryHackMe)", "category": "Deep Tech"},
                {"time": "12:30 PM - 02:30 PM", "activity": "Lunch, Walk, Rest Eyes & Social Break", "category": "Rest"},
                {"time": "02:30 PM - 05:00 PM", "activity": "⚡ Power Engine Sprint 2: FUNAAB Lecture Notes Revision & Code commits", "category": "University"},
                {"time": "05:00 PM - 09:30 PM", "activity": "Personal Freedom Time, Friends, Laundry, Chores & Relaxation", "category": "Life"},
                {"time": "10:00 PM - 08:00 AM", "activity": "Deep Sleep Reset", "category": "Sleep"}
            ]

scheduler = ShiftScheduler()
