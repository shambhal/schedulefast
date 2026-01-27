from datetime import date
from models import DoctorSpecial
from utils.time_utils import parse_hours

WEEKDAY_FIELD = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

def get_doctor_hours_for_date(db, doctor, target_date: date):
    # 1️⃣ Special day override
    special = db.query(DoctorSpecial).filter(
        DoctorSpecial.doctor_id == doctor.id,
        DoctorSpecial.sdate == target_date
    ).first()

    if special:
        if special.off:
            return []
        return parse_hours(special.hours)

    # 2️⃣ Weekly schedule
    weekday = target_date.weekday()
    field_name = WEEKDAY_FIELD[weekday]
    hours_str = getattr(doctor, field_name)

    if not hours_str or doctor.off:
        return []

    return parse_hours(hours_str)
