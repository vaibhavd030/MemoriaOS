"use client";

import { useState, useEffect, useRef } from "react";
import { Volume2, VolumeX, Play, Pause } from "lucide-react";

interface AudioPlayerProps {
  url: string;
  autoPlay?: boolean;
  onEnded?: () => void;
}

export default function AudioPlayer({ url, autoPlay = false, onEnded }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (autoPlay && audioRef.current) {
      audioRef.current.play().catch(err => console.error("Autoplay failed:", err));
    }
  }, [autoPlay, url]);

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) audioRef.current.pause();
      else audioRef.current.play();
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="flex items-center gap-4 glass p-3 rounded-2xl animate-fade-in">
      <button 
        onClick={togglePlay}
        className="w-10 h-10 rounded-full bg-accent-primary/20 flex items-center justify-center text-accent-primary"
      >
        {isPlaying ? <Pause size={18} /> : <Play size={18} />}
      </button>
      
      <div className="flex-1 h-1 bg-white/10 rounded-full overflow-hidden">
        <div className="h-full bg-accent-primary animate-pulse w-1/3" />
      </div>

      <button onClick={() => setIsMuted(!isMuted)} className="text-text-secondary">
        {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
      </button>

      <audio 
        ref={audioRef} 
        src={url} 
        muted={isMuted}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={onEnded}
        className="hidden"
      />
    </div>
  );
}
