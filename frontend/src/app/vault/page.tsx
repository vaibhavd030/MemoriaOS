"use client";

import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { Lock, FileText, ImageIcon, Database, ArrowRight } from "lucide-react";
import { getVault } from "@/lib/api";
import { motion } from "framer-motion";

export default function Vault() {
  const [vaultData, setVaultData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getVault();
        setVaultData(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const items = [
    { icon: ImageIcon, label: "Memory Media", count: vaultData?.counts?.media || 0, color: "text-accent-secondary", bg: "bg-accent-secondary/10" },
    { icon: Database, label: "Structured Data", count: vaultData?.counts?.data || 0, color: "text-accent-vibrant", bg: "bg-accent-vibrant/10" },
    { icon: FileText, label: "Narrative Logs", count: vaultData?.counts?.documents || 0, color: "text-accent-primary", bg: "bg-accent-primary/10" },
  ];

  return (
    <>
      <main className="main-content animate-fade space-y-8">
        <header className="flex items-center gap-4 px-4 pt-4">
          <div className="p-3 rounded-2xl glass bg-white/5 border-white/10 text-text-tertiary shadow-xl">
            <Lock size={24} />
          </div>
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent italic">
            Vault
          </h1>
        </header>

        <section className="grid grid-cols-1 gap-4 px-4">
          {items.map((item, i) => (
            <motion.div 
               key={item.label}
               initial={{ opacity: 0, x: -20 }}
               animate={{ opacity: 1, x: 0 }}
               transition={{ delay: i * 0.1 }}
               className="glass-card flex items-center justify-between group cursor-pointer hover:border-white/20 active:scale-[0.98] transition-all"
            >
              <div className="flex items-center gap-5">
                <div className={`p-4 rounded-[1.5rem] glass ${item.bg} border-white/5 group-hover:scale-110 transition-transform`}>
                  <item.icon size={24} className={item.color} />
                </div>
                <div>
                  <h3 className="font-semibold text-lg text-text-primary tracking-tight">{item.label}</h3>
                  <p className="text-[10px] text-text-tertiary uppercase tracking-widest font-bold">
                    {loading ? "..." : `${item.count} items`}
                  </p>
                </div>
              </div>
              <div className="w-10 h-10 rounded-full border border-white/5 flex items-center justify-center text-text-tertiary group-hover:text-white group-hover:border-white/30 transition-all bg-white/5">
                <ArrowRight size={18} />
              </div>
            </motion.div>
          ))}
        </section>

        <div className="px-4">
          <div className="p-8 rounded-[2rem] glass bg-gradient-to-br from-white/5 to-transparent border border-white/5 text-center space-y-4">
            <div className="w-12 h-12 rounded-full glass bg-accent-vibrant/20 flex items-center justify-center mx-auto text-accent-vibrant">
               <Database size={24} />
            </div>
            <h4 className="text-sm font-bold uppercase tracking-widest text-text-secondary">System Health</h4>
            <p className="text-xs text-text-tertiary leading-relaxed">
              MemoriaOS is actively parsing and encrypting your life-logging stream from 4 connected sources.
            </p>
          </div>
        </div>

        <footer className="text-center pt-4 pb-24">
          <p className="text-[9px] text-text-tertiary uppercase tracking-[0.3em] opacity-40">
            Secure Retrieval Protocol v0.1
          </p>
        </footer>
      </main>
      <Navigation />
    </>
  );
}
