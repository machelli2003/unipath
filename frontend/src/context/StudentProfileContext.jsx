import { createContext, useContext, useState, useCallback } from "react";

import api from "@/services/apiClient";

const StudentProfileContext = createContext(null);

const initialProfile = {
  mode: null, // "official_results" | "awaiting_results" | "nov_dec"
  shs_program: "",
  subjects: [], // [{subject_name, grade}]
  original_subjects: [], // only used for nov_dec mode
  interests: [],
  skills: [], // [{skill_name, rating}]
  career_goals: [],
};

export function StudentProfileProvider({ children }) {
  const [profile, setProfile] = useState(initialProfile);
  const [onboardingStep, setOnboardingStep] = useState(0);
  const [isSaving, setIsSaving] = useState(false);

  const updateProfile = useCallback((patch) => {
    setProfile((prev) => ({ ...prev, ...patch }));
  }, []);

  const resetProfile = useCallback(() => {
    setProfile(initialProfile);
    setOnboardingStep(0);
  }, []);

  const saveProfile = useCallback(async () => {
    setIsSaving(true);
    try {
      const { data } = await api.put("/profile", profile);
      return data;
    } finally {
      setIsSaving(false);
    }
  }, [profile]);

  const fetchProfile = useCallback(async () => {
    const { data } = await api.get("/profile");
    setProfile((prev) => ({ ...prev, ...data }));
    return data;
  }, []);

  const value = {
    profile,
    updateProfile,
    resetProfile,
    saveProfile,
    fetchProfile,
    isSaving,
    onboardingStep,
    setOnboardingStep,
  };

  return (
    <StudentProfileContext.Provider value={value}>
      {children}
    </StudentProfileContext.Provider>
  );
}

export function useStudentProfile() {
  const ctx = useContext(StudentProfileContext);
  if (!ctx) {
    throw new Error("useStudentProfile must be used within a StudentProfileProvider");
  }
  return ctx;
}
