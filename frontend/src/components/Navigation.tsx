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
    <nav className="fixed bottom-0 left-0 right-0 glass h-20 border-t border-white/10 flex items-center justify-around px-4 z-50">
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
  );
}
