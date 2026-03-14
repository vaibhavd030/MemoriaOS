"use client";

import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, AlertCircle, X } from "lucide-react";
import { useEffect } from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error" | "info";
  isVisible: boolean;
  onClose: () => void;
}

export default function Toast({ message, type = "success", isVisible, onClose }: ToastProps) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(onClose, 4000);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.9 }}
          className="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-full glass border border-white/20 shadow-2xl flex items-center gap-3 min-w-[300px]"
        >
          {type === "success" && <CheckCircle className="text-accent-secondary" size={18} />}
          {type === "error" && <AlertCircle className="text-red-400" size={18} />}
          <span className="text-xs font-medium tracking-wide text-white/90">{message}</span>
          <button onClick={onClose} className="ml-auto opacity-40 hover:opacity-100 transition-opacity">
            <X size={14} />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
