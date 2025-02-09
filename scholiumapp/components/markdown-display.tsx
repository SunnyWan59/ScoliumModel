import Markdown from "react-markdown";

export function DisplayMarkdown({ markdown }: { markdown: string }) {
  return (
    <div className="markdown-wrapper">
      {markdown?.split("\n\n").map((section, index) => (
        <Markdown key={index}>
          {section}
        </Markdown>
      ))}

    </div>
  );
}