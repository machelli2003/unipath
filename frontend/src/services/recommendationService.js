import api from "./apiClient";

// Run the full recommendation engine
export async function runRecommendations(assessmentId) {
  const { data } = await api.post(
    "/api/recommend",
    { assessment_id: assessmentId },
    { params: { ai: true } }
  );
  return data;
}

export async function getRecommendations(assessmentId) {
  return runRecommendations(assessmentId);
}

// Get the latest saved recommendation
export async function getLatestRecommendations() {
  const { data } = await api.get("/api/recommend/latest");
  return data;
}

// Get detailed explanation for one course
export async function getCourseExplanation(courseId) {
  const { data } = await api.get(`/api/recommend/course/${courseId}`);
  return data;
}

// What-if simulator — modify grades and re-run
export async function simulateGrades(gradeOverrides) {
  const { data } = await api.post("/api/simulate", {
    grade_overrides: gradeOverrides
  });
  return data;
}

// Compare courses side-by-side
export async function compareCourses(courseIds) {
  const { data } = await api.post("/api/compare/courses", {
    course_ids: courseIds
  });
  return data;
}

// Compare universities side-by-side
export async function compareUniversities(shortNames) {
  const { data } = await api.post("/api/compare/universities", {
    short_names: shortNames
  });
  return data;
}

// Get all courses (with optional filters)
export async function getCourses(filters = {}) {
  const { data } = await api.get("/api/courses", { params: filters });
  return data;
}

// Get single course with cut-off history
export async function getCourseDetail(courseId) {
  const { data } = await api.get(`/api/courses/${courseId}`);
  return data;
}

// Get all universities
export async function getUniversities() {
  const { data } = await api.get("/api/universities");
  return data;
}

// Get single university with its courses
export async function getUniversityDetail(shortName) {
  const { data } = await api.get(`/api/universities/${shortName}`);
  return data;
}

// Get all careers
export async function getCareers() {
  const { data } = await api.get("/api/careers");
  return data;
}

// Get single career with matching courses
export async function getCareerDetail(careerKey) {
  const { data } = await api.get(`/api/careers/${careerKey}`);
  return data;
}

// Submit assessment snapshot
export async function submitAssessment(assessmentData) {
  const { data } = await api.post("/api/assess", assessmentData);
  return data;
}

// Generate a report
export async function generateReport() {
  const { data } = await api.post("/api/report/generate");
  return data;
}

// Get all reports for user
export async function getReports() {
  const { data } = await api.get("/api/report");
  return data;
}