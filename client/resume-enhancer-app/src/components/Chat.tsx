import React, { useState } from "react";
import type { ChatMessage } from "../types";

interface ChatProps {
  messages: ChatMessage[];
  onSend: (message: string) => void;
}

const Chat: React.FC<ChatProps> = ({ messages, onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div style={{ flex: 1 }}>
      <div style={{ height: 200, overflowY: "auto", border: "1px solid #ccc", marginBottom: 10 }}>
        {messages.map((msg, i) => (
          <div key={i}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <textarea rows={3} value={input} onChange={(e) => setInput(e.target.value)} />
      <br />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default Chat;
