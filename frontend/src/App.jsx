import { Routes, Route, Navigate } from "react-router-dom";

import ProtectedRoute from "@/routes/ProtectedRoute";
import AppLayout from "@/components/layout/AppLayout";

import LoginPage from "@/pages/auth/LoginPage";
import RegisterPage from "@/pages/auth/RegisterPage";

import HomePage from "@/pages/HomePage";
import UniversitiesGuidePage from "@/pages/UniversitiesGuidePage";
import CutOffPointsPage from "@/pages/CutOffPointsPage";
import RequirementsPage from "@/pages/RequirementsPage";
import OnboardingWizardPage from "@/pages/onboarding/OnboardingWizardPage";
import AssessmentPage from "@/pages/dashboard/AssessmentPage";
import DashboardPage from "@/pages/dashboard/DashboardPage";

import RecommendationResultsPage from "@/pages/recommendations/RecommendationResultsPage";

import CourseListPage from "@/pages/courses/CourseListPage";
import CourseDetailPage from "@/pages/courses/CourseDetailPage";
import ComparisonPage from "@/pages/courses/ComparisonPage";

import UniversityListPage from "@/pages/universities/UniversityListPage";
import UniversityDetailPage from "@/pages/universities/UniversityDetailPage";

import CareerExplorerPage from "@/pages/careers/CareerExplorerPage";
import WhatIfSimulatorPage from "@/pages/simulator/WhatIfSimulatorPage";
import ReportsPage from "@/pages/reports/ReportsPage";
import SettingsPage from "@/pages/settings/SettingsPage";
import UpgradePage from "@/pages/settings/UpgradePage";

import NotFoundPage from "@/pages/NotFoundPage";

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Onboarding + assessment (auth required, no sidebar shell) */}
      <Route
        path="/onboarding"
        element={
          <ProtectedRoute>
            <OnboardingWizardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessment"
        element={
          <ProtectedRoute>
            <AssessmentPage />
          </ProtectedRoute>
        }
      />

      {/* Main app shell (auth required) */}
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/recommendations" element={<RecommendationResultsPage />} />

        <Route path="/courses" element={<CourseListPage />} />
        <Route path="/courses/:name" element={<CourseDetailPage />} />
        <Route path="/compare" element={<ComparisonPage />} />

        <Route path="/universities" element={<UniversityListPage />} />
        <Route path="/universities/:name" element={<UniversityDetailPage />} />

        <Route path="/careers" element={<CareerExplorerPage />} />

        <Route path="/simulator" element={<WhatIfSimulatorPage />} />
        <Route path="/reports" element={<ReportsPage />} />

        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/settings/upgrade" element={<UpgradePage />} />
      </Route>

      <Route path="/" element={<HomePage />} />
      <Route path="/best-universities" element={<UniversitiesGuidePage />} />
      <Route path="/cut-off-points" element={<CutOffPointsPage />} />
      <Route path="/admission-requirements" element={<RequirementsPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
