import { useState, useRef, useEffect } from "react";

export default function ChatUI({ onSend }) {
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [onSend.messages, onSend.isTyping]);

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">

      {/* Header */}
      <div className="p-4 bg-gray-800 text-xl font-semibold border-b border-gray-700">
        Interview Practice Partner
      </div>

      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">

        {onSend.messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-xl px-4 py-3 rounded-lg text-sm leading-relaxed ${
              msg.sender === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-gray-700"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {/* Typing indicator */}
        {onSend.isTyping && (
          <div className="bg-gray-700 w-20 px-4 py-3 rounded-lg flex space-x-2">
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input area */}
      <div className="p-4 bg-gray-800 flex gap-3 border-t border-gray-700">

        <button
          onClick={onSend.viewReport}
          disabled={onSend.isTyping}
          className={`px-4 py-3 rounded-lg font-medium ${
            onSend.isTyping
              ? "bg-purple-500 opacity-50"
              : "bg-purple-600 hover:bg-purple-700"
          }`}
        >
          View Report
        </button>

        <input
          type="text"
          placeholder="Type your answer..."
          value={input}
          disabled={onSend.isTyping}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) =>
            e.key === "Enter" &&
            !onSend.isTyping &&
            onSend.sendMessage(input, setInput)
          }
          className="flex-1 px-4 py-3 rounded-lg bg-gray-700 text-white focus:outline-none disabled:opacity-50"
        />

        <button
          onClick={() => onSend.sendMessage(input, setInput)}
          disabled={onSend.isTyping}
          className={`px-5 py-3 rounded-lg font-medium ${
            onSend.isTyping
              ? "bg-blue-500 opacity-50"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          Send
        </button>

      </div>
    </div>
  );
}

