'use client';

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export default function Main() {
    return (
      <>
        <h1 className="flex h-[60px] bg-black text-white items-center px-10 text-2xl font-medium">
          Scholium
        </h1>
          <div
            className="w-500px h-[calc(100vh-60px)] flex-shrink-0"
            style={
              { 
                "--copilot-kit-background-color": "#E0E9FD",
                "--copilot-kit-secondary-color": "#000000",
                "--copilot-kit-secondary-contrast-color": "#FFFFFF",
                "--copilot-kit-primary-color": "#FFFFFF",
                "--copilot-kit-contrast-color": "#000000",
              } as any
            }
          >
            <CopilotChat
              className="h-full"
              onSubmitMessage={async (message) => {
                await new Promise((resolve) => setTimeout(resolve, 30));
              }}
              labels={{
                title: "Scholium",
                initial: "Hi! How can I assist you with your research today?",
              }}
            />
          </div>
      </>
    );
  }