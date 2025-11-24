import { useState } from "react";
import axios from "axios";
import ChatUI from "./components/ChatUI";
import ReportView from "./components/ReportView";
import RoleSelect from "./components/RoleSelect";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [report, setReport] = useState(null);
  const [showReport, setShowReport] = useState(false);
  const [role, setRole] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  const API_CHAT = "http://127.0.0.1:8000/chat";
  const API_REPORT = "http://127.0.0.1:8000/report";

  const startInterviewWithRole = (selectedRole) => {
    setRole(selectedRole);
  };

  const sendMessage = async (input, resetInput) => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    resetInput("");

    setIsTyping(true);

    try {
      const payload = {
        message: input,
        session_id: sessionId,
        role: role,
      };

      const res = await axios.post(API_CHAT, payload);
      const data = res.data;

      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Simulate natural typing delay
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: data.response.message },
        ]);
        setIsTyping(false);
      }, 800);

    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "⚠️ Error connecting to server" },
      ]);
      setIsTyping(false);
    }
  };

  const viewReport = async () => {
    if (!sessionId) return alert("Interview not started!");

    try {
      const res = await axios.post(API_REPORT, { session_id: sessionId });
      setReport(res.data.report);
      setShowReport(true);
    } catch (err) {
      console.error(err);
      alert("Error generating report");
    }
  };

  if (showReport && report) {
    return <ReportView report={report} onBack={() => setShowReport(false)} />;
  }

  if (!sessionId && !role) {
    return <RoleSelect onSelect={startInterviewWithRole} />;
  }

  return (
    <ChatUI onSend={{ messages, sendMessage, viewReport, isTyping }} />
  );
}

