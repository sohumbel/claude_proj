import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { ProcessingSection } from "@/components/ProcessingSection";
import { ResultSection } from "@/components/ResultSection";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { getJobStatus, getVideoUrl } from "@/lib/api";
import { toast } from "sonner";

type ProcessingStage = "analyzing" | "roasting" | "generating" | "complete" | null;

const Generate = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [processingStage, setProcessingStage] = useState<ProcessingStage>("analyzing");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const jobId = searchParams.get("jobId");

  // Poll backend for real processing status
  useEffect(() => {
    if (!jobId) {
      toast.error("No job ID provided");
      navigate("/");
      return;
    }

    let pollInterval: NodeJS.Timeout;

    const pollStatus = async () => {
      try {
        const status = await getJobStatus(jobId);

        // Map backend status to frontend stage
        if (status.status === "analyzing") {
          setProcessingStage("analyzing");
        } else if (status.status === "roasting") {
          setProcessingStage("roasting");
        } else if (status.status === "generating") {
          setProcessingStage("generating");
        } else if (status.status === "completed") {
          setProcessingStage("complete");
          setVideoUrl(getVideoUrl(jobId));

          // Stop polling
          if (pollInterval) {
            clearInterval(pollInterval);
          }

          toast.success("Your roast video is ready!");
        } else if (status.status === "failed") {
          setError(status.error || "Processing failed");
          toast.error(status.error || "Processing failed");

          // Stop polling
          if (pollInterval) {
            clearInterval(pollInterval);
          }
        }
      } catch (err) {
        console.error("Error polling status:", err);
        setError(err instanceof Error ? err.message : "Failed to get status");
        toast.error("Failed to get processing status");

        // Stop polling on error
        if (pollInterval) {
          clearInterval(pollInterval);
        }
      }
    };

    // Initial poll
    pollStatus();

    // Set up polling interval (every 2 seconds)
    pollInterval = setInterval(pollStatus, 2000);

    // Cleanup on unmount
    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [jobId, navigate]);

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
