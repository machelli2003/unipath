from datetime import datetime
from bson import ObjectId

from ..db.mongodb import get_db


class ReportService:
    """Generate and persist a plain-text recommendation report."""

    def generate(self, user_id: str, profile: dict, rec: dict) -> dict:
        db = get_db()

        top = (rec or {}).get("top_courses", [])[:5]
        lines = [
            "UniPath Ghana — Recommendation Report",
            f"Generated: {datetime.utcnow().strftime('%d %B %Y')}",
            "",
            "Student Profile",
            f"SHS Programme : {profile.get('shs_program', '—') if profile else '—'}",
            f"Aggregate     : {rec.get('student_aggregate', '—') if rec else '—'}",
            f"Mode          : {profile.get('mode', '—') if profile else '—'}",
            "",
            "Top Course Recommendations",
        ]

        for i, c in enumerate(top, 1):
            course_name = c.get("course_name") or c.get("name") or "Unknown course"
            university = c.get("university") or c.get("university_name") or "—"
            match_score = round(c.get("match_score", 0))
            admission_category = c.get("admission_category", "").upper() or "—"
            lines.append(
                f"{i}. {course_name} — {university} | Match: {match_score}% | Admission: {admission_category}"
            )

        report_text = "\n".join(lines)
        doc = {
            "_id": ObjectId(),
            "user_id": user_id,
            "title": f"Recommendation Report — {datetime.utcnow().strftime('%B %Y')}",
            "content": report_text,
            "created_at": datetime.utcnow(),
        }

        try:
            db.reports.insert_one(doc)
            saved = True
        except Exception:
            saved = False

        return {
            "message": "Report generated.",
            "report_id": str(doc["_id"]),
            "content": report_text,
            "saved": saved,
        }
