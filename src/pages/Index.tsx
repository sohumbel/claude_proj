import { useState } from "react";
import { Hero } from "@/components/Hero";
import { UploadSection } from "@/components/UploadSection";

const Index = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [showUpload, setShowUpload] = useState(false);
  const [backgroundVideo, setBackgroundVideo] = useState<string>("subway_surfer");

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
  };

  const handleBackgroundChange = (background: string) => {
    setBackgroundVideo(background);
  };

  return (
    <div className="min-h-screen bg-background">
      <Hero onGetStarted={handleGetStarted} />
      
      {showUpload && (
        <div id="upload-section">
          <UploadSection
            onFileUpload={handleFileUpload}
            uploadedFile={uploadedFile}
            onRemoveFile={handleRemoveFile}
            backgroundVideo={backgroundVideo}
            onBackgroundChange={handleBackgroundChange}
          />
        </div>
      )}
      
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
