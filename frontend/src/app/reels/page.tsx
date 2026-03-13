"use client";

import Navigation from "@/components/Navigation";
import { Play } from "lucide-react";

export default function Reels() {
  return (
    <>
      <main className="main-content animate-fade space-y-8">
        <header>
          <h1 className="text-3xl font-bold tracking-tight">Memory Reels</h1>
          <p className="text-text-secondary text-sm">Your week in motion</p>
        </header>

        <section className="grid grid-cols-1 gap-6">
          <div className="relative group rounded-3xl overflow-hidden aspect-[9/16] max-h-[500px] border border-white/10 glass shadow-2xl">
            {/* Simulated Video Thumbnail */}
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/20 to-black/80" />
            <div className="absolute inset-0 flex items-center justify-center">
              <button className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30 transform transition-transform group-hover:scale-110">
                <Play size={32} fill="white" />
              </button>
            </div>
            
            <div className="absolute bottom-6 left-6 right-6 space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-accent-primary">Weekly Retrospective</span>
              <h3 className="text-xl font-semibold">The Week of Growth</h3>
              <p className="text-xs text-white/60">March 6 - March 13 • 45s</p>
            </div>
          </div>
        </section>
      </main>
      <Navigation />
    </>
  );
}
