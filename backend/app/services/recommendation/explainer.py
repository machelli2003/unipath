"""
Builds deterministic 'why' bullet points for each course recommendation.
No AI involved — purely rule-based from scoring data.
"""
from .grade_converter import GradeConverter


def _performance_score(grade: str) -> float:
    """Normalize the current 1-9 WASSCE scale to a 0-100-style score."""
    try:
        raw = GradeConverter.to_score(grade)
    except Exception:
        return 0.0

    return round(100 - ((raw - 1) * 100 / 8), 2)


class Explainer:

    def build_why_points(
        self,
        profile: dict,
        course: dict,
        scores: dict,
        admission: dict,
    ) -> list[str]:
        points = []

        grades = profile.get("wassce_subjects", {})
        required = course.get("required_subjects", [])

        strong_subjects = []
        weak_subjects = []
        for subj in required:
            # Handle both string and dict representations of requirements
            if isinstance(subj, dict):
                subject_name = subj.get("subject_name")
            else:
                subject_name = subj
            
            if not subject_name:
                continue
                
            grade = grades.get(subject_name)
            if grade:
                score = _performance_score(grade)
                if score >= 75:
                    strong_subjects.append(f"{subject_name} ({grade})")
                elif score < 44:
                    weak_subjects.append(f"{subject_name} ({grade})")

        if strong_subjects:
            points.append(f"Strong grades in {', '.join(strong_subjects[:2])}")
        if weak_subjects:
            points.append(f"⚠️ Weak grade in {', '.join(weak_subjects[:1])} — consider improving")

        student_interests = set(profile.get("interests", []))
        course_interests = set(course.get("interest_tags", []))
        matched_interests = student_interests & course_interests

        INTEREST_LABELS = {
            "tech_computing": "Technology & Computing",
            "health_sciences": "Health Sciences",
            "engineering": "Engineering",
            "business": "Business",
            "arts": "Arts & Humanities",
            "social_sciences": "Social Sciences",
            "entrepreneurship": "Entrepreneurship",
        }

        if matched_interests:
            labels = [INTEREST_LABELS.get(i, i) for i in list(matched_interests)[:2]]
            points.append(f"Matches your interest in {' and '.join(labels)}")

        raw_skills = profile.get("skills", [])
        if isinstance(raw_skills, dict):
            student_skills = raw_skills
        else:
            student_skills = {}
            for skill in raw_skills or []:
                if isinstance(skill, dict):
                    name = skill.get("skill_name") or skill.get("name")
                    rating = skill.get("rating") or skill.get("value") or 0
                    if name:
                        student_skills[str(name).strip().lower()] = int(rating)

        required_skills = course.get("required_skills", [])

        SKILL_LABELS = {
            "analytical_thinking": "Analytical Thinking",
            "problem_solving": "Problem Solving",
            "mathematics": "Mathematics",
            "communication": "Communication",
            "leadership": "Leadership",
            "creativity": "Creativity",
            "teamwork": "Teamwork",
        }

        strong_skills = []
        for skill in required_skills:
            normalized_skill = str(skill).strip().lower().replace(" ", "_")
            if student_skills.get(normalized_skill, 0) >= 4:
                strong_skills.append(SKILL_LABELS.get(normalized_skill, str(skill)))
        if strong_skills:
            points.append(f"High {' and '.join(strong_skills[:2])} skill rating")

        student_careers = set(profile.get("career_goals", []))
        course_careers = set(course.get("career_paths", []))
        matched_careers = student_careers & course_careers

        CAREER_LABELS = {
            "software_engineer": "Software Engineering",
            "doctor": "Medicine",
            "nurse": "Nursing",
            "pharmacist": "Pharmacy",
            "lawyer": "Law",
            "engineer": "Engineering",
            "accountant": "Accounting",
            "data_scientist": "Data Science",
            "architect": "Architecture",
            "teacher": "Teaching",
            "entrepreneur": "Entrepreneurship",
        }

        if matched_careers:
            labels = [CAREER_LABELS.get(c, c) for c in list(matched_careers)[:2]]
            points.append(f"Supports your goal of becoming a {' or '.join(labels)}")

        category = admission.get("admission_category", "competitive")
        gap = admission.get("gap", 0)
        cut_off = admission.get("cut_off_aggregate", 0)

        if category == "safe":
            points.append(
                f"Your aggregate is {abs(gap)} points better than the cut-off ({cut_off}) — strong chance"
            )
        elif category == "competitive":
            points.append(
                f"Your aggregate is close to the cut-off ({cut_off}) — competitive but achievable"
            )
        else:
            points.append(
                f"Cut-off is {cut_off} — consider improving grades or applying as NOV/DEC"
            )

        return points

    def build_summary(self, course: dict, scores: dict, admission: dict) -> str:
        total = scores["total"]
        category = admission["admission_category"]
        uni = course.get("university_short", "")
        name = course.get("name", "")

        cat_phrase = {
            "safe": "a strong admission chance",
            "competitive": "a competitive admission chance",
            "reach": "a reach — consider improving your aggregate",
        }.get(category, "a competitive admission chance")

        return (
            f"{name} at {uni} is a {round(total)}% match for your profile "
            f"with {cat_phrase}."
        )
