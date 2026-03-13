"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Mic, Zap, Send, Camera, X } from "lucide-react";
import { useState, useRef } from "react";
import Navigation from "@/components/Navigation";
import { sendChatMessage, ChatResponsePart } from "@/lib/api";

export default function Home() {
  const [message, setMessage] = useState("");
  const [replies, setReplies] = useState<ChatResponsePart[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = async () => {
    if (!message && !selectedImage) return;
    setIsLoading(true);
    try {
      const res = await sendChatMessage(message, selectedImage || undefined);
      setReplies(res.response);
      setMessage("");
      setSelectedImage(null);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      setSelectedImage(e.target.files[0]);
    }
  };

  return (
    <>
      <main className="main-content flex flex-col items-center min-h-[80vh] animate-fade pt-20">
        <header className="fixed top-0 left-0 right-0 p-6 flex justify-between items-center z-10 w-full max-w-[480px] mx-auto bg-background/80 backdrop-blur-md">
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

        {/* Gemini Live Visualizer or Chat Output */}
        <div className="w-full max-w-[480px] flex flex-col gap-8 flex-1">
          <AnimatePresence mode="wait">
            {replies.length === 0 ? (
              <motion.div 
                key="visualizer"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="flex flex-col items-center gap-12 py-12"
              >
                <div className="relative">
                  {[1, 2, 3].map((i) => (
                    <motion.div
                      key={i}
                      className="absolute inset-0 rounded-full border border-accent-primary/20"
                      initial={{ scale: 1, opacity: 0.5 }}
                      animate={{ scale: [1, 1.5 + i * 0.2], opacity: [0.5, 0] }}
                      transition={{ duration: 2.5, repeat: Infinity, delay: i * 0.4, ease: "easeOut" }}
                    />
                  ))}
                  <motion.button 
                    className="w-32 h-32 rounded-full glass flex items-center justify-center relative z-10"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Mic size={40} className="text-accent-primary" />
                  </motion.button>
                </div>
                <div className="text-center space-y-2">
                  <h1 className="text-2xl font-semibold tracking-tight">How can I help you today?</h1>
                  <p className="text-text-secondary text-sm">Tap the mic or type a message below</p>
                </div>
              </motion.div>
            ) : (
              <motion.div 
                key="replies"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col gap-4 p-4"
              >
                {replies.map((part, idx) => (
                  <div key={idx} className="glass-card p-4 rounded-2xl">
                    {part.type === "text" ? (
                      <p className="text-sm leading-relaxed">{part.content}</p>
                    ) : (
                      <img 
                        src={`data:${part.mime_type || "image/png"};base64,${part.content}`} 
                        alt="AI Response" 
                        className="rounded-lg max-w-full"
                      />
                    )}
                  </div>
                ))}
                <button 
                  onClick={() => setReplies([])}
                  className="text-xs text-accent-primary font-bold uppercase tracking-widest mt-4 self-center"
                >
                  New Memory
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Input Area */}
        <div className="fixed bottom-24 left-0 right-0 p-6 w-full max-w-[480px] mx-auto z-20">
          <div className="glass rounded-3xl p-2 flex flex-col gap-2 shadow-2xl">
            {selectedImage && (
              <div className="px-3 pt-2 flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase text-accent-primary truncate max-w-[200px]">
                  📎 {selectedImage.name}
                </span>
                <button onClick={() => setSelectedImage(null)}>
                  <X size={14} className="text-text-secondary" />
                </button>
              </div>
            )}
            <div className="flex items-center gap-2">
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="p-3 rounded-full hover:bg-white/5 transition-colors text-text-secondary"
              >
                <Camera size={20} />
              </button>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleImageSelect} 
                className="hidden" 
                accept="image/*"
              />
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Write a memory..."
                className="flex-1 bg-transparent border-none outline-none text-sm py-3 px-2"
              />
              <button 
                onClick={handleSend}
                disabled={isLoading}
                className={`p-3 rounded-2xl transition-all ${
                  isLoading ? "bg-white/5 opacity-50" : "bg-accent-primary text-background hover:scale-105 active:scale-95"
                }`}
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-background/30 border-t-background rounded-full animate-spin" />
                ) : (
                  <Send size={20} />
                )}
              </button>
            </div>
          </div>
        </div>
      </main>
      <Navigation />
    </>
  );
}
