import { useNavigate } from "react-router-dom";
import { useStudentProfile } from "@/context/StudentProfileContext";

import ModeSelectStep from "@/components/onboarding/ModeSelectStep";
import AcademicInfoStep from "@/components/onboarding/AcademicInfoStep";
import InterestsStep from "@/components/onboarding/InterestsStep";
import SkillsStep from "@/components/onboarding/SkillsStep";
import CareerGoalsStep from "@/components/onboarding/CareerGoalsStep";
import WizardProgressBar from "@/components/onboarding/WizardProgressBar";

const STEPS = [
  { key: "mode", label: "Mode", component: ModeSelectStep },
  { key: "academic", label: "Academics", component: AcademicInfoStep },
  { key: "interests", label: "Interests", component: InterestsStep },
  { key: "skills", label: "Skills", component: SkillsStep },
  { key: "careers", label: "Career Goals", component: CareerGoalsStep },
];

export default function OnboardingWizardPage() {
  const { onboardingStep, setOnboardingStep, saveProfile } = useStudentProfile();
  const navigate = useNavigate();

  const StepComponent = STEPS[onboardingStep].component;
  const isLastStep = onboardingStep === STEPS.length - 1;

  const handleNext = async () => {
    if (isLastStep) {
      await saveProfile();
      navigate("/assessment");
    } else {
      setOnboardingStep((s) => s + 1);
    }
  };

  const handleBack = () => {
    if (onboardingStep > 0) setOnboardingStep((s) => s - 1);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center px-4 py-10">
      <div className="w-full max-w-2xl space-y-8">
        <WizardProgressBar steps={STEPS} currentStep={onboardingStep} />

        <div className="rounded-lg border border-border bg-card p-6">
          <StepComponent />
        </div>

        <div className="flex justify-between">
          <button
            onClick={handleBack}
            disabled={onboardingStep === 0}
            className="rounded-md border border-input px-4 py-2 text-sm disabled:opacity-40"
          >
            Back
          </button>
          <button
            onClick={handleNext}
            className="rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm font-medium"
          >
            {isLastStep ? "Finish" : "Continue"}
          </button>
        </div>
      </div>
    </div>
  );
}
