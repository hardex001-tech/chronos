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
            energy_level = "Moderate"
            energy_desc = "Light maintenance (30-45 mins). Evening quick review. Rest early."
            next_phase_name = "Night Shift"
            days_to_next = 3 - cycle_day_idx
        elif 3 <= cycle_day_idx <= 5:
            shift_type = "Night"
            sub_day = cycle_day_idx - 2  # 1, 2, or 3
            badge_color = "#8B5CF6"  # Purple
            icon = "🌙"
            energy_level = "Low / Inverted"
            energy_desc = "Survival & Recovery. Zero forced coding. Sleep prioritized."
            next_phase_name = "Power Off-Days"
            days_to_next = 6 - cycle_day_idx
        else:
            shift_type = "Off"
            sub_day = cycle_day_idx - 5  # 1, 2, or 3
            badge_color = "#10B981"  # Emerald Green
            icon = "⚡"
            energy_level = "Maximum Power"
            energy_desc = "Deep Work Power Window (2 hours). Full energy for labs & building."
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
        """Generate tailored 24-hour itinerary matching current shift circadian rhythm."""
        if shift_type == "Morning":
            return [
                {"time": "06:00 - 07:30", "activity": "Morning Routine & Commute to Morning Shift", "category": "Work"},
                {"time": "08:00 - 15:00", "activity": "Morning Work Shift & University Lectures", "category": "Work/School"},
                {"time": "15:30 - 18:00", "activity": "Return to Hostel, Rest, Dinner & Reset", "category": "Rest"},
                {"time": "18:30 - 19:30", "activity": "FUNAAB School Lecture Notes & Review", "category": "Study"},
                {"time": "20:00 - 20:45", "activity": "Chronos Golden Window: 1 Google Cloud / Coursera Topic", "category": "Tech"},
                {"time": "21:30 - 06:00", "activity": "Uninterrupted Sleep (Protect your energy)", "category": "Rest"}
            ]
        elif shift_type == "Night":
            return [
                {"time": "08:00 - 15:30", "activity": "MANDATORY RECOVERY SLEEP (Do not disturb)", "category": "Rest"},
                {"time": "16:00 - 17:30", "activity": "Wake up, Hydrate, Healthy Meal & Light Air", "category": "Health"},
                {"time": "18:00 - 19:00", "activity": "Optional: Listen to 1 OSINT/Cyber Podcast or Audio lesson", "category": "Light"},
                {"time": "20:00 - 07:00", "activity": "Night Shift Operations (Stay hydrated & alert)", "category": "Work"}
            ]
        else:  # Off days
            return [
                {"time": "08:00 - 09:30", "activity": "Natural Wake-Up, Breakfast & Day Planning", "category": "Health"},
                {"time": "10:00 - 12:00", "activity": "⚡ Power Engine Sprint 1: Hands-on Labs (AWS / OSINT)", "category": "Tech"},
                {"time": "12:00 - 14:00", "activity": "Lunch, Walk, Rest Eyes & Social Break", "category": "Rest"},
                {"time": "14:30 - 16:30", "activity": "⚡ Power Engine Sprint 2: Code / GitHub Commit / Lecture prep", "category": "Tech"},
                {"time": "17:00 - 21:00", "activity": "Personal Freedom Time, Friends, Laundry, Chores", "category": "Life"},
                {"time": "22:00 - 07:00", "activity": "Deep Sleep Reset", "category": "Rest"}
            ]

scheduler = ShiftScheduler()
