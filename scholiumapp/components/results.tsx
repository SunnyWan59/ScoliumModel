"use client";

import { useChatContext } from "../lib/chat-context";
import { motion } from "framer-motion";
import { useCoAgent } from "@copilotkit/react-core";
import { DisplayMarkdown } from "./markdown-display";
import { ResearchState} from "../lib/agent-state";
import SelectCitation from "./ui/select"
import { useStyleContext } from "../lib/citation-context";
import CopyToClipboard from "./ui/copy-button";
import HomeButton from "./ui/home_button";
import LoadingState from "./ui/loading-state";
import { Box, Progress } from "@radix-ui/themes";
import { useState, useEffect} from "react";


export function Results() {
  const { researchQuery } = useChatContext();
  const { style} = useStyleContext();
  const { state: agentState } = useCoAgent<ResearchState>({
    name: "research_agent"
  });
  const {papers, setPapers} = useStyleContext();
  console.log(agentState?.answer?.results)


  return (
    <motion.div
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -50 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <div className="max-w-[1000px] p-8 lg:p-5 flex flex-col gap-y-8 mt-4 lg:mt-6 text-sm lg:text-base">

        <div className="flex items-center gap-20">
          <h1 className="text-3xl lg:text-4xl font-extralight">
            {researchQuery}
          </h1>
        </div>

        <div>
          {!agentState?.answer?.results && (
            // <LoadingState message="Finding Documents"/>
            <Box maxWidth="300px">
              <Progress />
            </Box>
          )}
        </div>
        {/* 
        Results from the model 
        */}
        <div className="grid grid-cols-12 gap-8">
          <div className="col-span-12 lg:col-span-8 flex flex-col">
            <div className="text-slate-700 font-light">
                {agentState?.answer?.results?.map((result, index) => (
                  <DisplayMarkdown 
                    key={index}
                    title={result.title}
                    contents={result.summary}
                    idx = {index}
                    results = {agentState?.answer?.results}
                  />
                ))}
            </div>
          </div>

        {/* 
        Citations
        */}
        
          {agentState?.answer?.results && (
            <div className="flex col-span-12 lg:col-span-4 flex-col gap-y-4 w-[200px]">
              <h2 className="flex items-center gap-x-2">
                <div className="flex items-center gap-x-2">
                    <p>References</p>
                    <SelectCitation/>
                </div>

              </h2>
              <ul className="text-slate-900 font-light text-sm flex flex-col gap-y-2">           
              {papers.map(
                  (ref: any, idx: number) => {
                    return (
                      <li key={idx}>
                        <a
                          href={ref.metadata?.doi}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          {idx + 1}. {ref.metadata?.title || "Untitled Reference"}
                        </a>
                      </li>
                    );
                  }
                )}

                {/* <li className="w-48">
                    <CopyToClipboard/>
                </li> */}
              </ul>
            </div>
          )}

          {/*
            For debugging purposes  
           */}
          {/* <div>
            {agentState?.answer?.paper_metadata&& (
              <pre>
                {JSON.stringify(agentState?.answer?.paper_metadata, null, 2)}
              </pre>
            )}
          </div> */}
          
        </div>
      </div>
    </motion.div>
  );
}