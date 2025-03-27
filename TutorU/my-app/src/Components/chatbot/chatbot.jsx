import React from "react";
import useChatbot from "../../Hooks/useChatbot.js"
import "../../style/chatbot.css";

const Chatbot = () => {
  const { messages, input, setInput, sendMessage } = useChatbot();

  return (
    <div className="chat-container">
      <div className="chat-content">
      <h2 className= "intro">Let's Start Our Chat Here!!! 😆</h2>
        <div className="chat-box">
            
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="chat-input-container">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="chat-input"
          />
          <button onClick={sendMessage} className="chat-send-button">Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
