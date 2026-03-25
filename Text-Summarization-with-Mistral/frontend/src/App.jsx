import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import EditorPane from './components/EditorPane';
import SummaryPane from './components/SummaryPane';

function App() {
  const [sources, setSources] = useState([]);
  const [activeSourceId, setActiveSourceId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize with one empty source if list is empty
  useEffect(() => {
    if (sources.length === 0) {
      addSource();
    }
  }, []);

  const addSource = (title = '', content = '') => {
    const newSource = {
      id: Date.now().toString(),
      title: title || '',
      content: content || '',
      summary: '',
      timestamp: new Date().toISOString()
    };
    setSources(prev => [...prev, newSource]);
    setActiveSourceId(newSource.id);
    setError(null);
    return newSource.id;
  };

  const deleteSource = (id) => {
    const newSources = sources.filter(s => s.id !== id);
    setSources(newSources);
    if (activeSourceId === id) {
      setActiveSourceId(newSources.length > 0 ? newSources[newSources.length - 1].id : null);
    }
  };

  const updateActiveSource = (field, value) => {
    setSources(prev => prev.map(source => 
      source.id === activeSourceId ? { ...source, [field]: value } : source
    ));
  };

  const activeSource = sources.find(s => s.id === activeSourceId);

  const handleSummarize = async () => {
    if (!activeSource || activeSource.content.length < 50) return;

    setIsLoading(true);
    setError(null);

    try {
      console.log('Summarizing text...');
      const response = await fetch('http://127.0.0.1:8000/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: activeSource.content }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Rate limit exceeded (5 per minute). Please wait a moment.');
        }
        throw new Error(data.detail || 'Failed to generate summary.');
      }

      updateActiveSource('summary', data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    console.log('Uploading file:', file.name);
    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/extract-text', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to extract text from file.');
      }

      // Create new source with extracted text
      addSource(data.filename, data.text);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-[#0f1117] text-gray-100 overflow-hidden font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      <Sidebar 
        sources={sources}
        activeSourceId={activeSourceId}
        onSelect={setActiveSourceId}
        onAdd={() => addSource()}
        onDelete={deleteSource}
        onUpload={handleFileUpload}
        isUploading={isUploading}
      />
      
      <main className="flex-1 flex overflow-hidden relative">
        <EditorPane 
          source={activeSource}
          onUpdate={updateActiveSource}
          onSummarize={handleSummarize}
          isLoading={isLoading}
          error={error}
        />
        
        <SummaryPane 
          summary={activeSource?.summary}
          error={error}
          onClose={() => {
            setError(null);
            updateActiveSource('summary', '');
          }}
        />
      </main>
    </div>
  );
}

export default App;
