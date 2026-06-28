"""
Master seed runner — runs all seed scripts in correct order.
Run: python -m scripts.seed_all  (from backend/)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.seed_universities import run as seed_universities
from scripts.seed_courses import run as seed_courses
from scripts.seed_cut_offs import run as seed_cut_offs
from scripts.seed_careers import run as seed_careers
from scripts.create_indexes import run as create_indexes

if __name__ == "__main__":
    print("\n🌱 UniPath Ghana — Database Seeding\n" + "=" * 45)

    print("\n[1/5] Universities...")
    seed_universities()

    print("\n[2/5] Courses...")
    seed_courses()

    print("\n[3/5] Cut-off points...")
    seed_cut_offs()

    print("\n[4/5] Careers...")
    seed_careers()

    print("\n[5/5] MongoDB indexes...")
    create_indexes()

    print("\n" + "=" * 45)
    print("✅ All seed data loaded successfully!")
    print("You can now run: python run.py")
