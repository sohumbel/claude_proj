import { Button } from "@/components/ui/button";
import { Flame } from "lucide-react";
import heroBg from "@/assets/hero-bg.jpg";

export const Hero = ({ onGetStarted }: { onGetStarted: () => void }) => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `url(${heroBg})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.2
        }}
      />
      
      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-subtle z-0" />
      
      {/* Content */}
      <div className="container relative z-10 px-4 py-20 text-center animate-fade-in">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Fire Icon */}
          <div className="flex justify-center mb-8">
            <div className="relative">
              <Flame className="w-20 h-20 text-primary animate-flame" />
              <div className="absolute inset-0 blur-xl bg-primary/50 animate-pulse-fire" />
            </div>
          </div>
          
          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
            Get Your Resume
            <span className="block bg-gradient-fire bg-clip-text text-transparent">
              Absolutely Roasted
            </span>
          </h1>
          
          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
            Upload your resume and watch as AI transforms it into a hilarious roast video. 
            Because sometimes you need to laugh at yourself.
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Button 
              variant="hero" 
              size="lg"
              onClick={onGetStarted}
              className="text-lg px-8 py-6 h-auto"
            >
              <Flame className="w-5 h-5" />
              Roast My Resume
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="text-lg px-8 py-6 h-auto border-primary/20 hover:border-primary/40"
            >
              See Example
            </Button>
          </div>
          
          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 pt-12 max-w-2xl mx-auto">
            <div className="space-y-2">
              <div className="text-3xl md:text-4xl font-bold text-primary">500+</div>
              <div className="text-sm text-muted-foreground">Resumes Roasted</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl md:text-4xl font-bold text-primary">10K+</div>
              <div className="text-sm text-muted-foreground">Laughs Generated</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl md:text-4xl font-bold text-primary">100%</div>
              <div className="text-sm text-muted-foreground">Ego Destroyed</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
