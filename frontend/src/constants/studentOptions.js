// Mirrors app/models/student_profile.py on the backend. Keep these two
// lists in sync — the recommendation engine validates against the
// backend's copy, but the frontend uses this for form dropdowns/wizards.

export const WASSCE_GRADES = ["A1", "B2", "B3", "C4", "C5", "C6", "D7", "E8", "F9"];

export const STUDENT_MODES = [
  { value: "official_results", label: "Official Results" },
  { value: "awaiting_results", label: "Awaiting Results" },
  { value: "nov_dec", label: "NOV/DEC / Improved Results" },
];

export const INTERESTS = [
  "Tech & Computing",
  "Health Sciences",
  "Engineering",
  "Business",
  "Arts",
  "Social Sciences",
  "Entrepreneurship",
];

export const SKILLS = [
  "Analytical Thinking",
  "Problem Solving",
  "Mathematics",
  "Communication",
  "Leadership",
  "Creativity",
  "Teamwork",
];

export const CAREER_GOALS = [
  "Software Engineer",
  "Doctor",
  "Lawyer",
  "Engineer",
  "Accountant",
  "Data Scientist",
];

export const ADMISSION_CATEGORIES = {
  SAFE: "Safe Choice",
  COMPETITIVE: "Competitive Choice",
  REACH: "Reach Choice",
};

export const COMMON_WASSCE_SUBJECTS = [
  "Mathematics",
  "English Language",
  "Integrated Science",
  "Social Studies",
  "Elective ICT",
  "Physics",
  "Chemistry",
  "Biology",
  "Economics",
  "Government",
  "Geography",
  "Literature in English",
  "French",
  "Elective Mathematics",
  "Financial Accounting",
  "Business Management",
];
