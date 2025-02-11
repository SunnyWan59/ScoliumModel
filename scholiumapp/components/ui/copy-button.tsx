import React, { useState } from 'react';

const CopyToClipboard: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const textToCopy = "This is the text that will be copied to your clipboard!";

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
      <p className="mb-4 text-gray-700">{textToCopy}</p>
      <button
        onClick={handleCopy}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
      >
        Copy to Clipboard
      </button>
      {copied && (
        <div className="mt-2 text-green-500">
          Copied!
        </div>
      )}
    </div>
  );
};

export default CopyToClipboard;