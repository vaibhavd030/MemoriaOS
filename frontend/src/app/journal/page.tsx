"use client";

import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { Plus, Search, Calendar, Clock } from "lucide-react";
import { getJournalRecords } from "@/lib/api";
import { motion } from "framer-motion";

export default function Journal() {
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getJournalRecords();
        setRecords(data.records);
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
        <header className="flex justify-between items-center px-4 pt-4">
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent italic">
            Journal
          </h1>
          <button className="p-3 rounded-full glass bg-accent-primary/10 text-accent-primary border-accent-primary/20 hover:scale-105 active:scale-95 transition-transform">
            <Plus size={20} />
          </button>
        </header>

        <div className="relative px-4">
          <Search className="absolute left-8 top-1/2 -translate-y-1/2 text-text-tertiary" size={18} />
          <input 
            type="text" 
            placeholder="Search memories..." 
            className="w-full glass bg-white/5 border-white/10 rounded-2xl py-4 pl-12 pr-4 outline-none focus:border-accent-primary/50 transition-all text-sm shadow-inner"
          />
        </div>

        <section className="space-y-4 px-4 pb-24">
          {loading ? (
             <div className="flex justify-center py-20">
                <div className="w-8 h-8 border-2 border-accent-primary/30 border-t-accent-primary rounded-full animate-spin" />
             </div>
          ) : records.length === 0 ? (
            <div className="text-center py-20 opacity-40">
              <Calendar size={48} className="mx-auto mb-4 stroke-1" />
              <p className="text-sm">No memories recorded yet.</p>
            </div>
          ) : records.map((record, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card hover:border-accent-primary/30 transition-colors group cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-accent-primary">
                  {record.type}
                </span>
                <div className="flex items-center gap-1 text-[10px] text-text-tertiary">
                  <Clock size={10} />
                  {record.date}
                </div>
              </div>
              <p className="text-sm leading-relaxed text-text-secondary group-hover:text-white transition-colors">
                {record.narrative || record.description || record.raw_text || JSON.stringify(record.data || record)}
              </p>
            </motion.div>
          ))}
        </section>
      </main>
      <Navigation />
    </>
  );
}
