"use client";

import { motion } from "framer-motion";
import { Mic, Zap } from "lucide-react";
import Navigation from "@/components/Navigation";

export default function Home() {
  return (
    <>
      <main className="main-content flex flex-col items-center justify-center min-h-[80vh] animate-fade">
        <header className="fixed top-0 left-0 right-0 p-6 flex justify-between items-center z-10 w-full max-w-[480px] mx-auto">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-accent-primary animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-[0.2em] text-text-secondary">
              Memoria OS
            </span>
          </div>
          <button className="p-2 rounded-full glass hover:bg-white/10 transition-colors">
            <Zap size={18} className="text-accent-vibrant" />
          </button>
        </header>

        {/* Gemini Live Visualizer */}
        <div className="relative flex flex-col items-center gap-12">
          <div className="relative">
            {/* Animated Rings */}
            {[1, 2, 3].map((i) => (
              <motion.div
                key={i}
                className="absolute inset-0 rounded-full border border-accent-primary/20"
                initial={{ scale: 1, opacity: 0.5 }}
                animate={{
                  scale: [1, 1.5 + i * 0.2],
                  opacity: [0.5, 0],
                }}
                transition={{
                  duration: 2.5,
                  repeat: Infinity,
                  delay: i * 0.4,
                  ease: "easeOut",
                }}
              />
            ))}
            
            <motion.div 
              className="w-32 h-32 rounded-full glass flex items-center justify-center relative z-10"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Mic size={40} className="text-accent-primary" />
            </motion.div>
          </div>

          <div className="text-center space-y-2">
            <h1 className="text-2xl font-semibold tracking-tight">How can I help you today?</h1>
            <p className="text-text-secondary text-sm">Tap the mic to start a live session</p>
          </div>
        </div>

        {/* Quick Context Cards */}
        <section className="w-full mt-16 grid grid-cols-2 gap-4">
          <div className="glass-card flex flex-col gap-2">
            <span className="text-[10px] font-bold uppercase text-accent-secondary">Health</span>
            <span className="text-lg font-medium">8h Sleep</span>
          </div>
          <div className="glass-card flex flex-col gap-2">
            <span className="text-[10px] font-bold uppercase text-accent-vibrant">Tasks</span>
            <span className="text-lg font-medium">3 Pending</span>
          </div>
        </section>
      </main>
      <Navigation />
    </>
  );
}
