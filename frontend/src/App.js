
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [currentField, setCurrentField] = useState(null);
  const [currentInterest, setCurrentInterest] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [showFieldOptions, setShowFieldOptions] = useState(false); // New state for initial options
  const [showInterestOptions, setShowInterestOptions] = useState(false); // New state for interest options

  // Ref for scrolling to the bottom of the chat
  const messageEndRef = useRef(null);

  // Scroll to the bottom whenever messages update
  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Initial bot greeting when the component mounts
  useEffect(() => {
    // Only send initial greeting if messages array is empty
    if (messages.length === 0) {
      simulateTypingEffect("Hey there! I'm here to help you explore career paths. What field are you interested in?", () => {
        setShowFieldOptions(true); // Show field options after initial greeting
      });
    }
  }, []); // Empty dependency array means this runs once on mount

  // Frontend representation of your career map, for displaying options
  // Note: Keys are lowercase to match backend logic
  const careerOptions = {
    science: [
      "coding", "physics", "biology", "chemistry",
      "mathematics", "earth science"
    ],
    arts: [
      "design", "writing", "music", "film",
      "performing arts"
    ],
    business: [
      "marketing", "finance", "entrepreneur",
      "management", "sales"
    ],
    engineering: [
      "mechanical", "civil", "electrical",
      "computer", "chemical", "aerospace"
    ],
    healthcare: [
      "medicine", "allied health", "mental health",
      "veterinary"
    ],
    law: [
      "legal practice", "judiciary", "public service"
    ],
    education: [
      "school", "higher education", "training"
    ],
    environment: [
      "ecology", "sustainability"
    ],
    sports: [
      "athletics", "support", "fitness"
    ],
    "social sciences": [ // Note the key for "social sciences"
      "human behavior", "public policy"
    ]
  };

  const simulateTypingEffect = (message, callback) => {
    let index = 0;
    setIsTyping(true);

    // Add a placeholder message for the bot *before* typing starts
    setMessages((prev) => [...prev, { sender: "bot", text: "" }]);

    const interval = setInterval(() => {
      setMessages((prev) => {
        // Find the last bot message and update its text
        const updatedMessages = [...prev];
        const lastBotMessageIndex = updatedMessages.length - 1;

        if (
          lastBotMessageIndex >= 0 &&
          updatedMessages[lastBotMessageIndex].sender === "bot"
        ) {
          updatedMessages[lastBotMessageIndex].text = message.slice(0, index + 1);
        }
        return updatedMessages;
      });

      index += 1;
      if (index === message.length) {
        clearInterval(interval);
        setIsTyping(false); // Stop typing animation
        callback();
      }
    }, 30); // Adjust typing speed to 30ms per character
  };

  const sendMessage = async (customMessage = null, addAsUserMessage = true) => {
    const messageToSend = customMessage !== null ? customMessage : input;

    // Prevent sending empty messages from input field if no custom message
    if (!messageToSend.trim() && customMessage === null) return;

    // Only add user message to chat display if addAsUserMessage is true
    if (addAsUserMessage) {
      setMessages((prev) => [...prev, { sender: "user", text: messageToSend }]);
    }
    setInput(""); // Clear input field

    try {
      // Send message to backend with current field and interest state
      const res = await axios.post("http://127.0.0.1:5000/ask", {
        message: messageToSend,
        field: currentField, // Pass currentField
        interest: currentInterest // Pass currentInterest
      });

      const botResponse = res.data.answer;
      const botChoices = res.data.choices; // Get choices from bot response

      simulateTypingEffect(botResponse, () => {
        // After typing, determine if new options should be shown
        if (botChoices && botChoices.length > 0) {
          if (!currentField) { // If user just selected a field, show interests
            setShowInterestOptions(true);
            setShowFieldOptions(false); // Hide field options once interest options are shown
          }
          // No explicit logic needed here for currentInterest and its roles,
          // as the backend directly provides the career list.
        } else {
            // If bot response doesn't come with choices, hide any active choice menus
            setShowFieldOptions(false);
            setShowInterestOptions(false);
        }
      });
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Oops! Something went wrong. Please try again." },
      ]);
      setIsTyping(false); // Ensure typing indicator is off on error
    }
  };

  const handleFieldSelection = (selectedField) => {
    setCurrentField(selectedField); // Set the current field
    setCurrentInterest(null); // Reset interest when a new field is chosen
    setShowFieldOptions(false); // Hide field options immediately

    // Add user's selected field to messages
    setMessages((prev) => [...prev, { sender: "user", text: capitalizeFirstLetter(selectedField) }]);

    // Trigger bot's response for the selected field
    sendMessage(selectedField, false); // false: Don't add to messages again
  };

  const handleInterestSelection = (selectedInterest) => {
    setCurrentInterest(selectedInterest); // Set the current interest
    setShowInterestOptions(false); // Hide interest options immediately

    // Add user's selected interest to messages
    setMessages((prev) => [...prev, { sender: "user", text: capitalizeFirstLetter(selectedInterest) }]);

    // Trigger bot's response for the selected interest
    sendMessage(selectedInterest, false); // false: Don't add to messages again
  };

  const resetConversation = () => {
    setMessages([]);
    setCurrentField(null);
    setCurrentInterest(null);
    setIsTyping(false);
    setInput("");
    setShowFieldOptions(true); // Show initial field options again
    setShowInterestOptions(false); // Ensure interest options are hidden
    // Re-send initial greeting if you want it after reset
    simulateTypingEffect("Hey there! I'm here to help you explore career paths. What field are you interested in?", () => {
      setShowFieldOptions(true);
    });
  };

  // Helper to capitalize first letter for display
  const capitalizeFirstLetter = (string) => {
    if (!string) return "";
    // Special case for "social sciences"
    if (string.toLowerCase() === "social sciences") {
      return "Social Sciences";
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "auto",
        padding: 20,
        background: "linear-gradient(135deg, #6e7dff, #82a1ff)",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
      }}
    >
      <h2 style={{ textAlign: "center", color: "#fff", marginBottom: 20 }}>Career Compass Bot</h2>

      {/* Message Area */}
      <div
        style={{
          border: "1px solid #ccc",
          height: 400,
          overflowY: "auto", // Changed to auto for better scroll behavior
          padding: 10,
          marginBottom: 20,
          borderRadius: "10px",
          backgroundColor: "#f9f9f9",
          boxShadow: "inset 0 1px 3px rgba(0,0,0,0.1)", // Inner shadow for depth
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              alignItems: "flex-start", // Align items to start for multi-line messages
              marginBottom: 15,
            }}
          >
            {msg.sender === "user" ? (
              <img
                src="https://img.icons8.com/ios/452/user-male-circle.png" // User icon
                alt="User"
                style={{ width: 30, height: 30, borderRadius: "50%", marginRight: 10, flexShrink: 0 }}
              />
            ) : (
              <img
                src="https://w7.pngwing.com/pngs/983/399/png-transparent-computer-icons-internet-bot-robot-robot-thumbnail.png" // Bot icon
                alt="Bot"
                style={{ width: 30, height: 30, borderRadius: "50%", marginLeft: 10, flexShrink: 0 }}
              />
            )}
            <div
              style={{
                backgroundColor: msg.sender === "user" ? "#4CAF50" : "#2196F3",
                color: "white",
                borderRadius: "10px",
                padding: "10px 15px",
                maxWidth: "70%",
                wordWrap: "break-word",
                lineHeight: "1.4",
                boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "center", marginBottom: 15 }}>
                <img
                    src="https://w7.pngwing.com/pngs/983/399/png-transparent-computer-icons-internet-bot-robot-robot-thumbnail.png"
                    alt="Bot"
                    style={{ width: 30, height: 30, borderRadius: "50%", marginLeft: 10, flexShrink: 0 }}
                />
                <div style={{
                    backgroundColor: "#e0e0e0",
                    color: "#333",
                    borderRadius: "10px",
                    padding: "10px 15px",
                    maxWidth: "70%",
                    wordWrap: "break-word",
                    lineHeight: "1.4",
                    fontStyle: "italic",
                    boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
                }}>
                    Bot is typing...
                </div>
            </div>
        )}
        <div ref={messageEndRef} /> {/* Scroll to bottom ref */}
      </div>

      {/* Field Selection */}
      {showFieldOptions && !currentField && (
        <div style={{ marginTop: 10 }}>
          <p style={{ color: "#fff", marginBottom: 10 }}>Choose a field to explore:</p>
          <ul style={{ listStyle: "none", paddingLeft: 0, display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {Object.keys(careerOptions).map((fld, idx) => (
              <li
                key={idx}
                style={{
                  cursor: "pointer",
                  backgroundColor: "#6a1b9a", // A nice purple for field buttons
                  color: "white",
                  padding: "8px 16px",
                  borderRadius: "20px", // More rounded
                  boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                  transition: "background-color 0.2s ease-in-out",
                  flexGrow: 1, // Allow items to grow to fill space
                  textAlign: "center",
                  minWidth: "120px" // Minimum width for buttons
                }}
                onClick={() => handleFieldSelection(fld)}
                onMouseEnter={(e) => (e.target.style.backgroundColor = "#7b1fa2")}
                onMouseLeave={(e) => (e.target.style.backgroundColor = "#6a1b9a")}
              >
                {capitalizeFirstLetter(fld)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Interest Selection */}
      {showInterestOptions && currentField && !currentInterest && (
        <div style={{ marginTop: 10 }}>
          <p style={{ color: "#fff", marginBottom: 10 }}>Which area of {capitalizeFirstLetter(currentField)} are you interested in?</p>
          <ul style={{ listStyle: "none", paddingLeft: 0, display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {careerOptions[currentField] && careerOptions[currentField].map((intr, idx) => (
              <li
                key={idx}
                style={{
                  cursor: "pointer",
                  backgroundColor: "#00796b", // A nice teal for interest buttons
                  color: "white",
                  padding: "8px 16px",
                  borderRadius: "20px", // More rounded
                  boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                  transition: "background-color 0.2s ease-in-out",
                  flexGrow: 1,
                  textAlign: "center",
                  minWidth: "120px"
                }}
                onClick={() => handleInterestSelection(intr)}
                onMouseEnter={(e) => (e.target.style.backgroundColor = "#00897b")}
                onMouseLeave={(e) => (e.target.style.backgroundColor = "#00796b")}
              >
                {capitalizeFirstLetter(intr)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Input Field and Send Button */}
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 20 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your question or query here..."
          disabled={isTyping}
          style={{
            flexGrow: 1, // Allows input to take available space
            padding: "12px",
            borderRadius: "8px", // Slightly more rounded
            border: "1px solid #ccc",
            marginRight: "10px",
            backgroundColor: isTyping ? "#e0e0e0" : "#fff",
            fontSize: "16px",
            outline: "none",
            boxShadow: "inset 0 1px 3px rgba(0,0,0,0.1)"
          }}
        />
        <button
          onClick={() => sendMessage()}
          disabled={isTyping || !input.trim()}
          style={{
            padding: "12px 25px",
            backgroundColor: isTyping || !input.trim() ? "#a5d6a7" : "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: isTyping || !input.trim() ? "not-allowed" : "pointer",
            fontWeight: "bold",
            transition: "background-color 0.3s ease-in-out",
            fontSize: "16px"
          }}
          onMouseEnter={(e) =>
            !isTyping && !input.trim()
              ? null
              : (e.target.style.backgroundColor = "#45a049")
          }
          onMouseLeave={(e) =>
            !isTyping && !input.trim()
              ? null
              : (e.target.style.backgroundColor = "#4CAF50")
          }
        >
          Send
        </button>
      </div>

      {/* Reset Button */}
      <button
        onClick={resetConversation}
        style={{
          width: "100%",
          marginTop: "10px",
          padding: "10px 20px",
          backgroundColor: "#FF5722",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "bold",
          transition: "background-color 0.3s",
          fontSize: "16px"
        }}
        onMouseEnter={(e) => (e.target.style.backgroundColor = "#e64a19")}
        onMouseLeave={(e) => (e.target.style.backgroundColor = "#FF5722")}
      >
        Start New Conversation
      </button>
    </div>
  );
}

export default App;
