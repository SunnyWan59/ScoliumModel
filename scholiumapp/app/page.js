import { CopilotChat } from "@copilotkit/react-ui";
import { CopilotSidebar } from "@copilotkit/react-ui";
import Main from "./main";


require('dotenv').config();
const publicApiKey = process.env.COPILOTKIT_API_KEY;


export default function Home() {
  return (
    <div className="w-100% h-100%">
      <Main/>
    </div>
    
  );
}
