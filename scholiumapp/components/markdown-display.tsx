import Markdown from "react-markdown";

export function DisplayMarkdown({ markdown }: { markdown: string }) {
  return (
    <div className="markdown-wrapper list-decimal space-y-8 [&>p]:mb-8">
        <Markdown>
          {markdown}
        </Markdown>

    </div>
  );
}