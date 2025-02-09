"use client";

import { useChatContext } from "../lib/chat-context";
import { motion } from "framer-motion";
import { useCoAgent } from "@copilotkit/react-core";
import { DisplayMarkdown } from "./markdown-display";
import { ResearchState} from "../lib/agent-state";

function addNewlines(text: string): string {
  if (!text) return "";
  return text.replace(/\n/g, "\n\n");
}


export function Results() {
  const { researchQuery } = useChatContext();
  const { state: agentState } = useCoAgent<ResearchState>({
    name: "research_agent"
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -50 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <div className="max-w-[1000px] p-8 lg:p-4 flex flex-col gap-y-8 mt-4 lg:mt-6 text-sm lg:text-base">
        <div className="space-y-4">
          <h1 className="text-3xl lg:text-4xl font-extralight">
            {researchQuery}
          </h1>
        </div>


        <div className="grid grid-cols-12 gap-8">
          <div className="col-span-12 lg:col-span-8 flex flex-col">
            <h2 className="flex items-center gap-x-2">
            </h2>
            <div className="text-slate-700 font-light">

                  <DisplayMarkdown markdown={addNewlines(agentState?.answer)} />

            </div>
          </div>


          {/* {agentState?.answer?.references?.length && (
            <div className="flex col-span-12 lg:col-span-4 flex-col gap-y-4 w-[200px]">
              <h2 className="flex items-center gap-x-2">
                References
              </h2>
              <ul className="text-slate-900 font-light text-sm flex flex-col gap-y-2">
                {agentState?.answer?.references?.map(
                  (ref: any, idx: number) => (
                    <li key={idx}>
                      <a
                        href={ref.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {idx + 1}. {ref.title}
                      </a>
                    </li>
                  )
                )}
              </ul>
            </div>
          )} */}
        </div>
      </div>
    </motion.div>
  );
}