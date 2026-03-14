"use client";

import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { Play, Film, AlertCircle } from "lucide-react";
import { getReels } from "@/lib/api";
import { motion } from "framer-motion";

export default function Reels() {
  const [reels, setReels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getReels();
        setReels(data.reels || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <>
      <main className="main-content animate-fade space-y-8">
        <header className="px-4 pt-4">
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent italic">
            Memory Reels
          </h1>
          <p className="text-text-secondary text-xs uppercase tracking-widest mt-1 opacity-60">Your week in motion</p>
        </header>

        <section className="grid grid-cols-1 gap-6 px-4 pb-24">
          {loading ? (
             <div className="flex justify-center py-20">
                <div className="w-8 h-8 border-2 border-accent-secondary/30 border-t-accent-secondary rounded-full animate-spin" />
             </div>
          ) : reels.length === 0 ? (
            <div className="text-center py-20 opacity-30">
              <Film size={48} className="mx-auto mb-4 stroke-1" />
              <p className="text-sm italic">No cinematic reels generated yet.</p>
            </div>
          ) : reels.map((reel, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 }}
              className="relative group rounded-[2rem] overflow-hidden aspect-[9/16] max-h-[500px] border border-white/10 glass shadow-2xl hover:border-accent-secondary/50 transition-all cursor-pointer bg-black"
            >
              <video 
                src={reel.url} 
                className="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity"
                loop
                muted
                playsInline
                onMouseOver={(e) => (e.target as HTMLVideoElement).play()}
                onMouseOut={(e) => (e.target as HTMLVideoElement).pause()}
              />
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/10 to-black/90" />
              
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <div className="w-16 h-16 rounded-full bg-white/10 backdrop-blur-xl flex items-center justify-center text-white border border-white/20">
                  <Play size={24} fill="currentColor" className="ml-1" />
                </div>
              </div>
              
              <div className="absolute bottom-8 left-8 right-8 space-y-3">
                <span className="inline-block px-3 py-1 rounded-full bg-accent-secondary/20 border border-accent-secondary/30 text-[8px] font-bold uppercase tracking-[0.2em] text-accent-secondary backdrop-blur-md">
                  Weekly Highlight
                </span>
                <h3 className="text-2xl font-bold tracking-tight">{reel.name.split('/').pop()}</h3>
                <p className="text-[10px] text-white/50 tracking-wide">
                  {new Date(reel.updated).toLocaleDateString()} • {(reel.size / 1024 / 1024).toFixed(1)}MB
                </p>
              </div>
            </motion.div>
          ))}
        </section>
      </main>
      <Navigation />
    </>
  );
}
