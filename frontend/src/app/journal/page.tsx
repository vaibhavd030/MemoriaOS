"use client";

import Navigation from "@/components/Navigation";
import { Plus, Search } from "lucide-react";

export default function Journal() {
  return (
    <>
      <main className="main-content animate-fade space-y-8">
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold tracking-tight">Journal</h1>
          <button className="p-3 rounded-full glass bg-accent-primary/10 text-accent-primary border-accent-primary/20">
            <Plus size={20} />
          </button>
        </header>

        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-tertiary" size={18} />
          <input 
            type="text" 
            placeholder="Search memories..." 
            className="w-full glass bg-white/5 border-white/10 rounded-full py-3 pl-12 pr-4 outline-none focus:border-accent-primary/50 transition-colors text-sm"
          />
        </div>

        <section className="space-y-4">
          <div className="glass-card space-y-3">
            <div className="flex justify-between items-start">
              <span className="text-[10px] font-bold uppercase tracking-widest text-accent-secondary">Yesterday</span>
              <span className="text-[10px] text-text-tertiary">2:30 PM</span>
            </div>
            <p className="text-sm leading-relaxed text-text-secondary">
              Had a deep reflection on the week's progress. Feeling energized by the new architecture. 
              The transition to Gemini 2.0 has been seamless...
            </p>
          </div>

          <div className="glass-card space-y-3">
            <div className="flex justify-between items-start">
              <span className="text-[10px] font-bold uppercase tracking-widest text-accent-vibrant">March 12</span>
              <span className="text-[10px] text-text-tertiary">10:15 AM</span>
            </div>
            <p className="text-sm leading-relaxed text-text-secondary">
              Morning meditation session was particularly insightful. Logged 20 minutes. 
              Focusing on mental clarity today.
            </p>
          </div>
        </section>
      </main>
      <Navigation />
    </>
  );
}
