require('dotenv').config();
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
          
        </Theme>
      </div>
    
  );
}
