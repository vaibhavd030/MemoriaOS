"use client";

import { Home, BookOpen, Film, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { icon: Home, label: "Live", href: "/" },
  { icon: BookOpen, label: "Journal", href: "/journal" },
  { icon: Film, label: "Reels", href: "/reels" },
  { icon: ShieldCheck, label: "Vault", href: "/vault" },
];

export default function Navigation() {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Bottom Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass h-20 border-t border-white/10 flex items-center justify-around px-4 z-50 md:hidden">
        <div className="max-w-[480px] w-full flex items-center justify-around">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center gap-1 transition-colors ${
                  isActive ? "text-accent-primary" : "text-text-secondary hover:text-text-primary"
                }`}
              >
                <item.icon size={24} strokeWidth={isActive ? 2.5 : 2} />
                <span className="text-[10px] font-medium uppercase tracking-wider">
                  {item.label}
                </span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Desktop Sidebar */}
      <nav className="fixed left-0 top-0 bottom-0 w-24 glass border-r border-white/10 hidden md:flex flex-col items-center py-12 gap-12 z-50">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center text-white font-bold text-xl shadow-lg mb-4">
          M
        </div>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center gap-2 transition-all p-4 rounded-2xl ${
                isActive ? "text-accent-primary bg-accent-primary/10 shadow-inner" : "text-text-secondary hover:text-white hover:bg-white/5"
              }`}
            >
              <item.icon size={28} strokeWidth={isActive ? 2.5 : 2} />
              <span className="text-[8px] font-bold uppercase tracking-[0.2em]">
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
