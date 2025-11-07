import { Card } from "@/components/ui/card";
import { Loader2, FileText, Sparkles, Video } from "lucide-react";

interface ProcessingSectionProps {
  stage: "analyzing" | "roasting" | "generating" | "complete" | null;
}

export const ProcessingSection = ({ stage }: ProcessingSectionProps) => {
  if (!stage) return null;

  const stages = [
    {
      id: "analyzing",
      icon: FileText,
      title: "Analyzing Resume",
      description: "Reading through your experience...",
    },
    {
      id: "roasting",
      icon: Sparkles,
      title: "Generating Roast",
      description: "AI is cooking up some heat...",
    },
    {
      id: "generating",
      icon: Video,
      title: "Creating Video",
      description: "Animating your roast...",
    },
  ];

  const currentIndex = stages.findIndex((s) => s.id === stage);

  return (
    <section className="py-20 px-4 animate-fade-in">
      <div className="container max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            {stage === "complete" ? "Your Roast is Ready! 🔥" : "Processing Your Resume"}
          </h2>
          <p className="text-muted-foreground text-lg">
            {stage === "complete"
              ? "Scroll down to watch your epic roast"
              : "This will only take a moment..."}
          </p>
        </div>

        {stage !== "complete" && (
          <div className="space-y-6">
            {stages.map((stageItem, index) => {
              const Icon = stageItem.icon;
              const isActive = index === currentIndex;
              const isComplete = index < currentIndex;

              return (
                <Card
                  key={stageItem.id}
                  className={`p-6 transition-all duration-500 ${
                    isActive
                      ? "border-primary bg-primary/5 scale-105"
                      : isComplete
                      ? "border-primary/30 bg-card/50"
                      : "border-border opacity-50"
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`p-3 rounded-lg transition-all ${
                        isActive
                          ? "bg-primary text-primary-foreground"
                          : isComplete
                          ? "bg-primary/20 text-primary"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {isActive ? (
                        <Loader2 className="w-6 h-6 animate-spin" />
                      ) : (
                        <Icon className="w-6 h-6" />
                      )}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{stageItem.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {stageItem.description}
                      </p>
                    </div>
                    {isComplete && (
                      <div className="text-primary text-2xl">✓</div>
                    )}
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
};
