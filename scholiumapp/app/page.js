import { CopilotChat } from "@copilotkit/react-ui";
import { CopilotSidebar } from "@copilotkit/react-ui";
import {HomeView} from "../components/home"
import { ChatContextProvider } from "../lib/chat-context";
import {HomeResearch} from "../components/research-home"
import { StyleContextProvider } from "../lib/citation-context";
require('dotenv').config();
const publicApiKey = process.env.COPILOTKIT_API_KEY;
import "@radix-ui/themes/styles.css";
import { Theme } from "@radix-ui/themes";

export default function Page() {
  return(
    <Home/>
  );
}

function Home() {
  return (
      <div className="w-100% h-100%">
        <Theme accentColor="brown" grayColor="sand" radius="full">
        {/* <Main/> */}
          <ChatContextProvider>
            <StyleContextProvider>
              <HomeResearch/>
            </StyleContextProvider>
          </ChatContextProvider>
        </Theme>
      </div>
    
  );
}
