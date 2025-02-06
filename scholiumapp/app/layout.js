import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core"; 
import "@copilotkit/react-ui/styles.css";


require('dotenv').config();
const publicApiKey = process.env.COPILOTKIT_API_KEY;


export const metadata = {
  title: "Scholium",
  description: "Your own research assistant",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="w-screen h-screen">
        <CopilotKit 
          runtimeUrl="/api/copilotkit"
          
        > 
            {children}
        </CopilotKit>
      </body>
    </html>
  );
}
