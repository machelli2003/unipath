"""Unit tests for the new admission CutOffAnalyzer."""

from mongoengine import ConnectionFailure

from app.services.admission.cut_off_analyzer import CutOffAnalyzer


def test_analyze_uses_latest_cutoff(monkeypatch):
    analyzer = CutOffAnalyzer()
    monkeypatch.setattr(
        analyzer,
        "get_latest_cut_off",
        lambda course_id: {"aggregate": 21, "year": 2025},
    )

    result = analyzer.analyze({"_id": "course-1"}, student_aggregate=18)

    assert result["cut_off_aggregate"] == 21
    assert result["cut_off_year"] == 2025
    assert result["student_aggregate"] == 18
    assert result["admission_category"] == "safe"
    assert result["admission_probability"] == 85
    assert result["gap"] == -3


def test_analyze_falls_back_to_course_default_when_no_cutoff(monkeypatch):
    analyzer = CutOffAnalyzer()
    monkeypatch.setattr(analyzer, "get_latest_cut_off", lambda course_id: None)

    result = analyzer.analyze({"_id": "course-1", "cut_off_2025": 24}, student_aggregate=25)

    assert result["cut_off_aggregate"] == 24
    assert result["cut_off_year"] == 2025
    assert result["admission_category"] == "competitive"
    assert result["admission_probability"] == 35


def test_get_latest_cut_off_returns_none_when_db_is_unavailable(monkeypatch):
    analyzer = CutOffAnalyzer()

    def raise_connection_failure(_course_id):
        raise ConnectionFailure("No default connection")

    monkeypatch.setattr("app.services.admission.cut_off_analyzer.get_db", raise_connection_failure)

    assert analyzer.get_latest_cut_off("course-1") is None
