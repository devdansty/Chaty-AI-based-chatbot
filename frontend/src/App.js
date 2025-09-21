import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages([...messages, userMessage]);

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });

      const botMessage = { sender: "bot", text: res.data.response };
      setMessages([...messages, userMessage, botMessage]);
    } catch (err) {
      console.error(err);
    }

    setInput("");
  };

  const deleteTask = async (task) => {
    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: `delete task ${task}`,
      });
      const botMessage = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      <div className="tasks-panel">
        <div className="tasks-header">Tasks</div>
        <div className="tasks-list">
          {messages.some(
            (msg) => msg.sender === "bot" && msg.text.includes("Your tasks")
          ) ? (
            messages
              .filter((msg) => msg.sender === "bot" && msg.text.includes("Your tasks"))
              .map((msg, index) =>
                msg.text
                  .split("\n")
                  .slice(1)
                  .map((task, i) => (
                    <div key={`${index}-${i}`} className="task-item">
                      <span>{task.replace("- ", "")}</span>
                      <button
                        onClick={() => deleteTask(task.replace("- ", ""))}
                        className="delete-btn"
                      >
                        Delete
                      </button>
                    </div>
                  ))
              )
          ) : (
            <p>No tasks yet</p>
          )}
        </div>
      </div>

      <div className="chat-panel">
        <div className="chat-header">
          <h1>Chaty</h1>
          <p>By Sameer</p>
        </div>

        <div className="chat-area">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              <div className={`message-bubble ${msg.sender}`}>
                {msg.text.split("\n").map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="input-bar">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}
