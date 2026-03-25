import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Check, X, Quote } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const SummaryPane = ({ summary, onClose, error }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <AnimatePresence>
      {(summary || error) && (
        <motion.div
          initial={{ x: 400, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 400, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="w-[400px] border-l border-gray-800 bg-[#161922] flex flex-col h-full shadow-2xl relative z-10"
        >
          <div className="p-4 border-b border-gray-800 flex items-center justify-between bg-gray-900/50">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold">
              <Quote size={18} />
              <span>Summary</span>
            </div>
            <div className="flex items-center gap-1">
              {summary && (
                <button
                  onClick={handleCopy}
                  className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-gray-200 transition-colors"
                  title="Copy to clipboard"
                >
                  {copied ? <Check size={18} className="text-green-500" /> : <Copy size={18} />}
                </button>
              )}
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-gray-200 transition-colors"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
            {error ? (
              <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-400 text-sm">
                <div className="font-bold mb-1 flex items-center gap-2">
                  <X size={14} /> Error
                </div>
                {error}
              </div>
            ) : (
              <div className="prose prose-invert prose-indigo max-w-none prose-p:text-gray-300 prose-headings:text-indigo-300 prose-strong:text-indigo-200 prose-ul:text-gray-300">
                <ReactMarkdown>{summary}</ReactMarkdown>
              </div>
            )}
          </div>

          <div className="p-4 bg-indigo-600/5 border-t border-gray-800 text-[10px] text-gray-500 text-center italic">
            Mistral Large Language Model Output
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default SummaryPane;
