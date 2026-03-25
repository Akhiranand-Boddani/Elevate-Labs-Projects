import React from 'react';
import { Plus, FileText, Trash2, BookOpen, Upload, Loader2 } from 'lucide-react';

const Sidebar = ({ sources, activeSourceId, onSelect, onAdd, onDelete, onUpload, isUploading }) => {
  const fileInputRef = React.useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onUpload(file);
      event.target.value = null; // Reset input
    }
  };

  return (
    <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col h-full overflow-hidden shrink-0">
      <div className="p-4 border-b border-gray-800 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-indigo-400">
          <BookOpen size={20} />
          <span>NotebookAI</span>
        </div>
      </div>

      <div className="p-4 space-y-2">
        <button
          onClick={onAdd}
          className="w-full flex items-center justify-center gap-2 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 py-2 rounded-lg transition-all text-sm font-medium group"
        >
          <Plus size={16} className="group-hover:rotate-90 transition-transform" />
          New Source
        </button>
        
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className="w-full flex items-center justify-center gap-2 bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 py-2 rounded-lg transition-all text-sm font-medium group disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isUploading ? (
            <Loader2 size={16} className="animate-spin text-indigo-400" />
          ) : (
            <Upload size={16} className="group-hover:-translate-y-0.5 transition-transform" />
          )}
          {isUploading ? 'Uploading...' : 'Upload Document'}
        </button>
        
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
          className="hidden"
        />
      </div>

      <div className="flex-1 overflow-y-auto px-2 space-y-1 custom-scrollbar">
        <div className="px-2 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Sources ({sources.length})
        </div>
        {sources.length === 0 ? (
          <div className="px-4 py-8 text-center text-gray-600 text-sm">
            No sources yet.<br/>Add one to start.
          </div>
        ) : (
          sources.map((source) => (
            <div
              key={source.id}
              className={`group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-all ${
                activeSourceId === source.id
                  ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/20'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
              }`}
              onClick={() => onSelect(source.id)}
            >
              <div className="flex items-center gap-2 overflow-hidden">
                <FileText size={16} className="shrink-0" />
                <span className="truncate text-sm font-medium">
                  {source.title || 'Untitled Source'}
                </span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(source.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 hover:text-red-400 rounded transition-all"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))
        )}
      </div>

      <div className="p-4 border-t border-gray-800">
        <div className="text-[10px] text-gray-600 text-center uppercase tracking-widest font-bold">
          Powered by Mistral AI
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
