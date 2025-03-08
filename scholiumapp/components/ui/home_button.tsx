"use-client";

import React, { useState } from 'react';
import { Button } from "@radix-ui/themes";

import { useRouter } from 'next/navigation';

const HomeButton: React.FC = () => {
  const router = useRouter();

  const handleNavigateHome = () => {
    window.location.reload();
  };

  return (
    <div className="p-4">
      <Button
        onClick={handleNavigateHome}
        className="flex items-center gap-2 absolute right-4"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        
        Home
      </Button>
    </div>
  );
};

export default HomeButton;
