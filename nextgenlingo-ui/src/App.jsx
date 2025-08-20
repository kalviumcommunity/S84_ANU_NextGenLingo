import React, { useState, useRef, useEffect } from "react";
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
} from "@mui/material";

import ReactMarkdown from "react-markdown";

// Mode selector component for unique chat modes
function ModeSelector({ mode, setMode }) {
  return (
    <FormControl fullWidth sx={{ mb: 2 }}>
      <InputLabel id="mode-select-label">Choose Chat Mode</InputLabel>
      <Select
        labelId="mode-select-label"
        value={mode}
        label="Choose Chat Mode"
        onChange={(e) => setMode(e.target.value)}
      >
        <MenuItem value="quiz">Quiz</MenuItem>
        <MenuItem value="flashcards">Flashcards</MenuItem>
        <MenuItem value="summary">Summary</MenuItem>
        <MenuItem value="code_review">Code Review</MenuItem>
        <MenuItem value="debate">Debate</MenuItem>
        <MenuItem value="interactive_tutorial">Interactive Tutorial</MenuItem>
      </Select>
    </FormControl>
  );
}

/** Quiz component inline in chat */
function Quiz({ questions, onComplete }) {
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  const handleChange = (qid, ans) => {
    setAnswers((prev) => ({ ...prev, [qid]: ans }));
  };

  const handleSubmit = () => {
    setShowResults(true);
    if (onComplete) onComplete(answers);
  };

  return (
    <Box sx={{ mt: 1, mb: 2, p: 1, bgcolor: "#f0f7ff", borderRadius: 2 }}>
      {questions.map((q, idx) => (
        <Box key={idx} mb={2}>
          <Typography sx={{ fontWeight: "600" }}>
            {idx + 1}. {q.question}
          </Typography>
          <RadioGroup
            value={answers[q.id] || ""}
            onChange={(e) => handleChange(q.id, e.target.value)}
          >
            {q.options.map((opt, i) => (
              <FormControlLabel
                key={i}
                value={opt}
                control={<Radio />}
                label={opt}
                disabled={showResults}
              />
            ))}
          </RadioGroup>
          {showResults && (
            <Typography
              variant="body2"
              color={answers[q.id] === q.answer ? "green" : "error"}
            >
              Correct answer: {q.answer}
            </Typography>
          )}
        </Box>
      ))}
      {!showResults && (
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={Object.keys(answers).length < questions.length}
        >
          Submit Answers
        </Button>
      )}
    </Box>
  );
}

/** Citation chips component */
function CitationChips({ sources }) {
  if (!sources || sources.length === 0) return null;
  return (
    <Box mt={1}>
      {sources.map((src, i) => (
        <Chip
          key={i}
          label={src}
          size="small"
          color="info"
          sx={{ mr: 1, cursor: "pointer" }}
          onClick={() => window.open(src, "_blank")}
        />
      ))}
    </Box>
  );
}

function App() {
  const [chatMode, setChatMode] = useState("summary"); // default mode
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const BACKEND_URL = "http://localhost:8000";
  const bottomRef = useRef(null);

  // Auto-scroll chat to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = async () => {
    if (!query.trim()) return;
    setLoading(true);
    // Add user message to chat
    setChat((prev) => [...prev, { role: "user", content: query, type: "text" }]);
    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, intent: chatMode }),
      });
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();

      // Handle different response types
      if (data.type === "quiz" && data.questions) {
        setChat((prev) => [
          ...prev,
          { role: "assistant", type: "quiz", questions: data.questions, sources: data.sources || [] },
        ]);
      } else {
        setChat((prev) => [
          ...prev,
          { role: "assistant", type: "text", content: data.response || "", sources: data.sources || [] },
        ]);
      }
    } catch (err) {
      setChat((prev) => [
        ...prev,
        { role: "bot", type: "text", content: `Error: ${err.message}`, sources: [] },
      ]);
    }
    setQuery("");
    setLoading(false);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      alert("Document uploaded and processed!");
      e.target.value = null;
    } catch (err) {
      alert(err.message);
    }
  };

const renderMessage = (msg, idx) => {
  // Defensive check for null or missing type
  if (!msg || !msg.type) {
    return (
      <ListItem key={idx}>
        <ListItemText primary={<em>Received invalid response from server.</em>} />
      </ListItem>
    );
  }
  
  switch (msg.type) {
    case "quiz":
      return (
        <Quiz
          key={idx}
          questions={msg.questions}
          onComplete={(answers) => alert("Quiz submitted!")}
        />
      );
    case "text":
    default:
      return (
        <ListItem
          key={idx}
          alignItems="flex-start"
          sx={{
            flexDirection: msg.role === "user" ? "row-reverse" : "row",
            textAlign: msg.role === "user" ? "right" : "left",
          }}
        >
          <ListItemText
            primary={
              <Typography
                component="span"
                variant="subtitle2"
                color={msg.role === "user" ? "primary" : "secondary"}
              >
                {msg.role === "user" ? "You" : "Bot"}
              </Typography>
            }
            secondaryTypographyProps={{ component: "div" }}
            secondary={
              <div style={{ marginTop: 8 }}>
                <ReactMarkdown>{msg.content || msg.response || ""}</ReactMarkdown>
                <CitationChips sources={msg.sources} />
              </div>
            }
          />
        </ListItem>
      );
  }
};


  return (
    <Container
      maxWidth="sm"
      sx={{
        mt: 5,
        border: "1px solid #2196f3",
        borderRadius: 2,
        p: 3,
        backgroundColor: "#f0f7ff",
      }}
    >
      <Typography variant="h4" align="center" gutterBottom color="primary">
        NextGenLingo
      </Typography>

      <Button variant="contained" component="label" sx={{ mb: 2 }}>
        📂 Upload Document
        <input hidden type="file" onChange={handleFileChange} />
      </Button>

      <ModeSelector mode={chatMode} setMode={setChatMode} />

      <Paper
        elevation={3}
        sx={{ height: 400, overflowY: "auto", p: 2, mb: 2, backgroundColor: "#ffffff" }}
      >
        <List>
          {chat.map((msg, idx) => (
            <React.Fragment key={idx}>
              {renderMessage(msg, idx)}
              <Divider />
            </React.Fragment>
          ))}
          {loading && (
            <ListItem>
              <ListItemText primary={<em>Bot: typing...</em>} />
            </ListItem>
          )}
          <div ref={bottomRef} />
        </List>
      </Paper>

      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your question here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <Button onClick={sendMessage} variant="contained" disabled={loading || !query.trim()}>
          Send
        </Button>
      </Box>
    </Container>
  );
}

export default App;
