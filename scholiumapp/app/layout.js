import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core"; 


require('dotenv').config();
const publicApiKey = process.env.COPILOTKIT_API_KEY;

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Scholium",
  description: "Your own research assistant",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <CopilotKit publicApiKey="<your-copilot-cloud-public-api-key>"> 
            {children}
        </CopilotKit>
      </body>
    </html>
  );
}
