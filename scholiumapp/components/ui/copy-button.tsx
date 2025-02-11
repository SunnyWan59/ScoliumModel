"use-client";

import React, { useState } from 'react';
import { useCoAgent } from "@copilotkit/react-core";
import { ResearchState } from '../../lib/agent-state';

const CopyToClipboard: React.FC = () => {
  const { state: agentState } = useCoAgent<ResearchState>({
    name: "research_agent"
  });
  const [copied, setCopied] = useState(false);
  const textToCopy = agentState?.answer?.markdown;

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