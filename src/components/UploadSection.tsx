import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, File, X, Flame } from "lucide-react";
import { toast } from "sonner";
import { uploadResume } from "@/lib/api";

interface UploadSectionProps {
  onFileUpload: (file: File) => void;
  uploadedFile: File | null;
  onRemoveFile: () => void;
  backgroundVideo: string;
  onBackgroundChange: (background: string) => void;
}

export const UploadSection = ({
  onFileUpload,
  uploadedFile,
  onRemoveFile,
  backgroundVideo,
  onBackgroundChange
}: UploadSectionProps) => {
  const navigate = useNavigate();
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        onFileUpload(file);
        toast.success("Resume uploaded successfully!");
      } else {
        toast.error("Please upload a PDF file");
      }
    }
  }, [onFileUpload]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        onFileUpload(file);
        toast.success("Resume uploaded successfully!");
      } else {
        toast.error("Please upload a PDF file");
      }
    }
  };

  const handleGenerateRoast = async () => {
    if (!uploadedFile) {
      toast.error("No file uploaded");
      return;
    }

    setIsUploading(true);

    try {
      // Upload file to backend with selected background video and get job_id
      const response = await uploadResume(uploadedFile, backgroundVideo);

      toast.success("Upload successful! Generating roast...");

      // Navigate to generate page with job_id
      navigate(`/generate?jobId=${response.job_id}`);
    } catch (error) {
      console.error("Upload error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to upload resume");
      setIsUploading(false);
    }
  };

  return (
    <section className="py-20 px-4">
      <div className="container max-w-3xl mx-auto">
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Upload Your Resume
          </h2>
          <p className="text-muted-foreground text-lg">
            Drop your PDF resume below and let the roasting begin
          </p>
        </div>

        {!uploadedFile ? (
          <Card
            className={`p-12 border-2 border-dashed transition-all duration-300 ${
              isDragging
                ? "border-primary bg-primary/5 scale-105"
                : "border-border hover:border-primary/50"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center text-center space-y-6">
              <div className="relative">
                <Upload className="w-16 h-16 text-muted-foreground" />
                {isDragging && (
                  <div className="absolute inset-0 blur-xl bg-primary/30 animate-pulse" />
                )}
              </div>

              <div className="space-y-2">
                <p className="text-xl font-semibold">
                  Drag & drop your resume here
                </p>
                <p className="text-muted-foreground">
                  or click the button below to browse
                </p>
              </div>

              <Button
                variant="fire"
                size="lg"
                onClick={() => document.getElementById("file-upload")?.click()}
                className="mt-4"
              >
                <Upload className="w-5 h-5" />
                Choose File
              </Button>

              <input
                id="file-upload"
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleFileInput}
              />

              <p className="text-sm text-muted-foreground">
                Supported format: PDF (Max 10MB)
              </p>
            </div>
          </Card>
        ) : (
          <Card className="p-8 border-primary/30 bg-card/50 backdrop-blur animate-scale-in space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-primary/10 rounded-lg">
                  <File className="w-8 h-8 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-lg">{uploadedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={onRemoveFile}
                className="hover:bg-destructive/10 hover:text-destructive"
              >
                <X className="w-5 h-5" />
              </Button>
            </div>

            {/* Background Video Selector */}
            <div className="pt-4 border-t border-border space-y-4">
              <div>
                <label className="text-sm font-medium mb-3 block">
                  Choose Brainrot Background:
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  {["subway_surfer", "minecraft", "fortnite", "templerun", "satisfying"].map((bg) => (
                    <button
                      key={bg}
                      onClick={() => onBackgroundChange(bg)}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        backgroundVideo === bg
                          ? "border-primary bg-primary/10"
                          : "border-border hover:border-primary/50"
                      }`}
                    >
                      <div className="text-sm font-medium capitalize">
                        {bg.replace("_", " ")}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Generate Button */}
              <Button
                variant="hero"
                size="lg"
                onClick={handleGenerateRoast}
                disabled={isUploading}
                className="w-full text-lg"
              >
                <Flame className="w-5 h-5" />
                {isUploading ? "Uploading..." : "Generate Roast Video"}
              </Button>
              <p className="text-center text-sm text-muted-foreground">
                This will take approximately 30-60 seconds
              </p>
            </div>
          </Card>
        )}
      </div>
    </section>
  );
};
