"use-client";

import React, { useState } from 'react';
import { useCoAgent } from "@copilotkit/react-core";
import { ResearchState } from '../../lib/agent-state';
import { processAndGenerateCitations } from '../../lib/metadata-citations';
import { useStyleContext } from '../../lib/citation-context';

const CopyToClipboard: React.FC = () => {
  const { state: agentState } = useCoAgent<ResearchState>({
    name: "research_agent"
  });
  const { style} = useStyleContext();
  const [copied, setCopied] = useState(false);
  const citations = processAndGenerateCitations(agentState?.answer?.metadata, style).join('\n')
  
  const textToCopy = citations;
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);

      // Reset the copied status after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Failed to copy text:", error);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <button
        onClick={handleCopy}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
      >
        Copy to Clipboard
      </button>
    </div>
  );
};

export default CopyToClipboard;