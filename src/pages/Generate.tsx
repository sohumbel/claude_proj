import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ProcessingSection } from "@/components/ProcessingSection";
import { ResultSection } from "@/components/ResultSection";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

type ProcessingStage = "analyzing" | "roasting" | "generating" | "complete" | null;

const Generate = () => {
  const navigate = useNavigate();
  const [processingStage, setProcessingStage] = useState<ProcessingStage>("analyzing");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  // Simulate processing stages
  useEffect(() => {
    const processVideo = async () => {
      // Analyzing stage
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProcessingStage("roasting");
      
      // Roasting stage
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProcessingStage("generating");
      
      // Generating stage
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProcessingStage("complete");
      setVideoUrl("https://example.com/video.mp4"); // Placeholder
    };

    processVideo();
  }, []);

  const handleReset = () => {
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border py-6">
        <div className="container px-4">
          <Button
            variant="ghost"
            onClick={() => navigate("/")}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
        </div>
      </header>

      {/* Processing Section */}
      <ProcessingSection stage={processingStage} />
      
      {/* Result Section */}
      <ResultSection videoUrl={videoUrl} onReset={handleReset} />
      
      {/* Footer */}
      <footer className="border-t border-border py-8 mt-20">
        <div className="container text-center text-muted-foreground text-sm">
          <p>Made with 🔥 for those brave enough to laugh at themselves</p>
        </div>
      </footer>
    </div>
  );
};

export default Generate;
