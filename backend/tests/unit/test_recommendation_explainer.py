from app.services.recommendation.explainer import Explainer


def test_build_why_points_accepts_skills_as_list_of_dicts():
    explainer = Explainer()
    profile = {
        "wassce_subjects": {"Mathematics": "A1"},
        "interests": ["Tech & Computing"],
        "skills": [{"skill_name": "Problem Solving", "rating": 5}],
        "career_goals": ["Software Engineer"],
    }
    course = {
        "name": "Computer Science",
        "required_subjects": [{"subject_name": "Mathematics"}],
        "interest_tags": ["Tech & Computing"],
        "required_skills": ["Problem Solving"],
        "career_paths": ["Software Engineer"],
        "university_short": "UG",
    }
    scores = {"total": 90}
    admission = {"admission_category": "safe", "gap": 3, "cut_off_aggregate": 20}

    points = explainer.build_why_points(profile, course, scores, admission)

    assert isinstance(points, list)
    assert len(points) >= 1
