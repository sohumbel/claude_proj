import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Download, Share2, RotateCcw } from "lucide-react";
import { toast } from "sonner";

interface ResultSectionProps {
  videoUrl: string | null;
  onReset: () => void;
}

export const ResultSection = ({ videoUrl, onReset }: ResultSectionProps) => {
  if (!videoUrl) return null;

  const handleDownload = () => {
    toast.success("Download started!");
    // Add actual download logic here
  };

  const handleShare = () => {
    toast.success("Link copied to clipboard!");
    // Add actual share logic here
  };

  return (
    <section className="py-20 px-4 animate-fade-in">
      <div className="container max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Your Roast Video is Ready! 🔥
          </h2>
          <p className="text-muted-foreground text-lg">
            Share it with friends or keep it as a reminder to update that resume
          </p>
        </div>

        <Card className="p-8 space-y-8 border-primary/30 bg-card/50 backdrop-blur">
          {/* Video Player Placeholder */}
          <div className="relative aspect-video bg-muted rounded-lg overflow-hidden border-2 border-border">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center space-y-4">
                <div className="text-6xl">🎥</div>
                <p className="text-lg text-muted-foreground">
                  Video Player Placeholder
                </p>
                <p className="text-sm text-muted-foreground">
                  Your roast video would appear here
                </p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              variant="fire"
              size="lg"
              onClick={handleDownload}
              className="flex-1"
            >
              <Download className="w-5 h-5" />
              Download Video
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={handleShare}
              className="flex-1 border-primary/20 hover:border-primary/40"
            >
              <Share2 className="w-5 h-5" />
              Share
            </Button>
            <Button
              variant="ghost"
              size="lg"
              onClick={onReset}
              className="flex-1"
            >
              <RotateCcw className="w-5 h-5" />
              Roast Another
            </Button>
          </div>
        </Card>

        {/* Fun Stats */}
        <div className="mt-12 text-center">
          <p className="text-muted-foreground mb-4">Roast Statistics</p>
          <div className="grid grid-cols-3 gap-4 max-w-xl mx-auto">
            <Card className="p-4">
              <div className="text-2xl font-bold text-primary">87%</div>
              <div className="text-xs text-muted-foreground">Savage Level</div>
            </Card>
            <Card className="p-4">
              <div className="text-2xl font-bold text-primary">12</div>
              <div className="text-xs text-muted-foreground">Burns Delivered</div>
            </Card>
            <Card className="p-4">
              <div className="text-2xl font-bold text-primary">4.8</div>
              <div className="text-xs text-muted-foreground">Laugh Score</div>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};
