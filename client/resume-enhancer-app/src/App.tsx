import React, { useState } from "react";
import ResumePreview from "./components/ResumePreview";
import Chat from "./components/Chat";
import type { ChatMessage } from "./types";
import { sendEnhancementRequest } from "./api";
import 'react-pdf/dist/Page/TextLayer.css';
import 'react-pdf/dist/Page/AnnotationLayer.css';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [enhancedFile, setEnhancedFile] = useState<Blob | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f && f.type === "application/pdf") {
      setFile(f);
    }
  };

  const handleSend = async (input: string) => {
    if (!file) {
      alert("Please upload a resume first.");
      return;
    }

    const newMessages: ChatMessage[] = [...messages, { role: "user", content: input }];
    setMessages(newMessages);

    const { newMessage, enhancedBlob } = await sendEnhancementRequest(file, newMessages);

    setMessages([...newMessages, { role: "assistant", content: newMessage }]);
    setEnhancedFile(enhancedBlob);
  };

  return (
    <div style={{ display: "flex", gap: "2rem", padding: "2rem" }}>
      <div>
        <h2>Upload Resume</h2>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        {file && <ResumePreview file={file} />}
      </div>

      <div>
        <h2>Enhancement Chat</h2>
        <Chat messages={messages} onSend={handleSend} />
        {enhancedFile && (
          <>
            <h3>Enhanced Resume</h3>
            <ResumePreview file={enhancedFile} />
            <a href={URL.createObjectURL(enhancedFile)} download="enhanced_resume.pdf">
              📥 Download Enhanced Resume
            </a>
          </>
        )}
      </div>
    </div>
  );
};

export default App;