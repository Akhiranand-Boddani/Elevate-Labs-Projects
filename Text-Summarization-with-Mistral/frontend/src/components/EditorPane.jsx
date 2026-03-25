import React from 'react';
import { Sparkles, BarChart3, X } from 'lucide-react';

const EditorPane = ({ source, onUpdate, onSummarize, isLoading, error }) => {
  if (!source) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-[#0f1117] text-gray-500 p-8 text-center">
        <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mb-4">
          <Sparkles size={32} />
        </div>
        <h2 className="text-xl font-semibold text-gray-300">Select a source to begin</h2>
        <p className="max-w-xs mt-2">Choose an existing source from the sidebar or create a new one to start summarizing.</p>
      </div>
    );
  }

  const wordCount = source.content.trim() ? source.content.trim().split(/\s+/).length : 0;
  const charCount = source.content.length;

  return (
    <div className="flex-1 flex flex-col bg-[#0f1117] overflow-hidden">
      <div className="p-6 border-b border-gray-800 flex items-center justify-between bg-gray-900/30">
        <input
          type="text"
          value={source.title}
          onChange={(e) => onUpdate('title', e.target.value)}
          placeholder="Source Title"
          className="bg-transparent border-none text-xl font-bold text-gray-100 outline-none focus:ring-0 w-full placeholder-gray-700"
        />
        <button
          onClick={onSummarize}
          disabled={isLoading || charCount < 50}
          className={`flex items-center gap-2 px-6 py-2 rounded-full font-semibold transition-all shrink-0
            ${isLoading || charCount < 50
              ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
              : 'bg-indigo-500 hover:bg-indigo-400 text-white shadow-lg shadow-indigo-500/20 active:scale-95'
            }`}
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              <span>Processing...</span>
            </div>
          ) : (
            <>
              <Sparkles size={18} />
              <span>Summarize</span>
            </>
          )}
        </button>
      </div>

      <div className="flex-1 relative group p-6 flex flex-col">
        {error && (
          <div className="mb-4 bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-400 text-sm flex items-center gap-3 animate-in fade-in slide-in-from-top-2">
            <div className="shrink-0 w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center">
              <X size={16} />
            </div>
            <div className="flex-1">{error}</div>
          </div>
        )}
        <textarea
          value={source.content}
          onChange={(e) => onUpdate('content', e.target.value)}
          placeholder="Paste your text here (minimum 50 characters)..."
          className="w-full h-full bg-transparent border-none text-gray-300 text-lg leading-relaxed resize-none outline-none focus:ring-0 placeholder-gray-800 custom-scrollbar flex-1"
        ></textarea>
      </div>

      <div className="p-4 border-t border-gray-800 flex items-center justify-between text-xs text-gray-500 bg-gray-900/30 px-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <BarChart3 size={14} />
            <span>{wordCount} words</span>
          </div>
          <span>•</span>
          <span>{charCount} characters</span>
        </div>
        <div>
          {charCount < 50 && charCount > 0 && (
            <span className="text-orange-500/70 italic">Need {50 - charCount} more characters</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default EditorPane;
