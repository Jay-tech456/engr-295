import { useState, useEffect } from "react";

const useChatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hi! What physics concept can I help you with today?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Fetch response from local server
    const response = await fetchBackendResponse(input);
    setMessages((prev) => [...prev, { text: response, sender: "bot" }]);
  };

  const fetchBackendResponse = async (message) => {
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      return "Sorry, there was an issue connecting to the server.";
    }
  };

  return { messages, input, setInput, sendMessage };
};

export default useChatbot;
