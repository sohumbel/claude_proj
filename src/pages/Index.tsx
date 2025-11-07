import { useState } from "react";
import { Hero } from "@/components/Hero";
import { UploadSection } from "@/components/UploadSection";
import { ProcessingSection } from "@/components/ProcessingSection";
import { ResultSection } from "@/components/ResultSection";

type ProcessingStage = "analyzing" | "roasting" | "generating" | "complete" | null;

const Index = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [processingStage, setProcessingStage] = useState<ProcessingStage>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [showUpload, setShowUpload] = useState(false);

  const handleGetStarted = () => {
    setShowUpload(true);
    // Smooth scroll to upload section
    setTimeout(() => {
      document.getElementById("upload-section")?.scrollIntoView({ 
        behavior: "smooth",
        block: "start"
      });
    }, 100);
  };

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    setProcessingStage(null);
    setVideoUrl(null);
  };

  const handleReset = () => {
    setUploadedFile(null);
    setProcessingStage(null);
    setVideoUrl(null);
    setShowUpload(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Simulate processing stages (in real app, this would be triggered by actual API calls)
  const startProcessing = () => {
    setProcessingStage("analyzing");
    setTimeout(() => {
      setProcessingStage("roasting");
      setTimeout(() => {
        setProcessingStage("generating");
        setTimeout(() => {
          setProcessingStage("complete");
          setVideoUrl("https://example.com/video.mp4"); // Placeholder
        }, 2000);
      }, 2000);
    }, 2000);
  };

  // Auto-start processing when file is uploaded
  useState(() => {
    if (uploadedFile && !processingStage) {
      startProcessing();
    }
  });

  return (
    <div className="min-h-screen bg-background">
      <Hero onGetStarted={handleGetStarted} />
      
      {showUpload && (
        <div id="upload-section">
          <UploadSection 
            onFileUpload={handleFileUpload}
            uploadedFile={uploadedFile}
            onRemoveFile={handleRemoveFile}
          />
        </div>
      )}
      
      <ProcessingSection stage={processingStage} />
      
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

export default Index;
