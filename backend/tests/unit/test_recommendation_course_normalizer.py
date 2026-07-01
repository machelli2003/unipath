from app.routes.recommendation_routes import _normalize_course_payload


def test_normalize_course_payload_handles_string_required_subjects():
    course = {
        "name": "Computer Science",
        "required_subjects": "Mathematics",
        "required_skills": "Programming",
        "related_interests": "Tech & Computing",
        "related_career_goals": "Software Engineer",
    }

    normalized = _normalize_course_payload(course)

    assert normalized["name"] == "Computer Science"
    assert normalized["required_subjects"][0]["subject_name"] == "Mathematics"
    assert normalized["required_skills"] == ["Programming"]
    assert normalized["related_interests"] == ["Tech & Computing"]
    assert normalized["related_career_goals"] == ["Software Engineer"]
