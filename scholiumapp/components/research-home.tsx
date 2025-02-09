"use client";

import { HomeView } from "./home";
import {Results} from "./results";
import { AnimatePresence } from "framer-motion";
import { useChatContext } from "../lib/chat-context";

export function HomeResearch() {
  const { researchQuery, setTextInput } = useChatContext();
  return (
    <>
      <div className="flex flex-col items-center justify-center relative z-10">
        <div className="flex-1">
          {researchQuery ? (
            <AnimatePresence
              key="results"
              onExitComplete={() => {
                setTextInput("");
              }}
              mode="wait"
            >
              <Results key="results" />
            </AnimatePresence>
          ) : (
            <AnimatePresence key="home" mode="wait">
              <HomeView key="home" />
            </AnimatePresence>
          )}
        </div>
      </div>
    </>
  );
}