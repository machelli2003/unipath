from app import create_app
from app.services.recommendation.engine import RecommendationEngine

app = create_app()
with app.app_context():
    engine = RecommendationEngine()
    
    test_profile = {
        "user_id": "test_user_123",
        "shs_program": "Science",
        "mode": "Day",
        "wassce_subjects": {
            "English": "A1",
            "Mathematics": "B2",
            "Physics": "B3",
            "Chemistry": "B3",
            "Biology": "B2",
            "Elective Mathematics": "C4"
        }
    }
    
    result = engine.run(test_profile, save=False)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"✓ Recommendation generated successfully")
        print(f"  Student aggregate: {result.get('student_aggregate')}")
        print(f"  SHS Program: {result.get('shs_program')}")
        print(f"  Top courses: {len(result.get('top_courses', []))} recommendations")
        if result.get('top_courses'):
            print(f"  1st recommendation: {result['top_courses'][0]['course_name']}")
            print(f"     Match score: {result['top_courses'][0]['match_score']}%")
            print(f"     Admission: {result['top_courses'][0]['admission_category']}")
