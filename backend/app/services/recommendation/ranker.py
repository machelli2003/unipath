"""
Ranks scored courses and returns the top N results.
Applies SHS programme eligibility filter before ranking.
"""


class Ranker:

    def filter_eligible(self, courses: list, shs_program: str) -> list:
        eligible = []
        for c in courses:
            allowed = c["course"].get("eligible_shs_programmes", [])
            if not allowed or shs_program in allowed:
                eligible.append(c)
        return eligible

    def rank(self, scored_courses: list, top_n: int = 10) -> list:
        sorted_courses = sorted(
            scored_courses,
            key=lambda x: x["scores"]["total"],
            reverse=True,
        )
        return sorted_courses[:top_n]

    def rank_with_filter(
        self,
        scored_courses: list,
        shs_program: str,
        top_n: int = 10,
    ) -> list:
        eligible = self.filter_eligible(scored_courses, shs_program)
        if len(eligible) < top_n:
            eligible = scored_courses
        return self.rank(eligible, top_n)
