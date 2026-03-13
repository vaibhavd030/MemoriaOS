"use client";

import Navigation from "@/components/Navigation";
import { Lock, FileText, Image as ImageIcon, Database } from "lucide-react";

const vaultItems = [
  { icon: FileText, label: "Documents", count: 12, color: "text-accent-primary" },
  { icon: ImageIcon, label: "Media", count: 156, color: "text-accent-secondary" },
  { icon: Database, label: "Structured Data", count: 42, color: "text-accent-vibrant" },
];

export default function Vault() {
  return (
    <>
      <main className="main-content animate-fade space-y-8">
        <header className="flex items-center gap-3">
          <Lock size={28} className="text-text-tertiary" />
          <h1 className="text-3xl font-bold tracking-tight">Vault</h1>
        </header>

        <section className="grid grid-cols-1 gap-4">
          {vaultItems.map((item) => (
            <div key={item.label} className="glass-card flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-2xl glass bg-white/5 border-white/10 group-hover:bg-white/10 transition-colors`}>
                  <item.icon size={24} className={item.color} />
                </div>
                <div>
                  <h3 className="font-medium text-text-primary">{item.label}</h3>
                  <p className="text-xs text-text-tertiary">{item.count} items</p>
                </div>
              </div>
              <div className="w-8 h-8 rounded-full border border-white/5 flex items-center justify-center text-text-tertiary group-hover:border-white/20 transition-all">
                →
              </div>
            </div>
          ))}
        </section>

        <footer className="text-center pt-8">
          <p className="text-[10px] text-text-tertiary uppercase tracking-widest">
            End-to-End Encrypted Selection
          </p>
        </footer>
      </main>
      <Navigation />
    </>
  );
}
