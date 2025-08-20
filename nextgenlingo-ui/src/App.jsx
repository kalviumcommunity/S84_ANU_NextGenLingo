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

/**
 * =======================
 *  GLOBAL LUXE CSS (pure CSS – no Tailwind)
 *  Injected once into <head> as a <style> tag.
 *  - Animated aurora background
 *  - Soft glassmorphism surfaces
 *  - Micro-interactions (hover/press)
 *  - Custom scrollbars
 *  - Polished chat bubbles + sent/received alignments
 * =======================
 */
const STYLES = `
  :root{
    --bg: #0a0c10;
    --glass: rgba(255,255,255,0.08);
    --glass-2: rgba(255,255,255,0.14);
    --txt: #e9eefb;
    --muted: #a9b2c7;
    --pri: #7aa2ff; /* primary accent */
    --pri-2: #a77bff; /* secondary accent */
    --ok: #4ad295;
    --err: #ff6b6b;
    --ring: rgba(122,162,255,0.35);
    --shadow: 0 10px 30px rgba(0,0,0,0.35);
    --radius-2xl: 22px;
    --radius-xl: 18px;
  }

  /* Aurora gradient background */
  body{
    background: radial-gradient(1200px 700px at 10% 10%, rgba(101,134,255,0.18), transparent 60%),
                radial-gradient(900px 600px at 100% 0%, rgba(167,123,255,0.15), transparent 60%),
                radial-gradient(800px 600px at 50% 100%, rgba(74,210,149,0.12), transparent 60%),
                linear-gradient(180deg, #0b0f17 0%, #0a0c10 100%);
    color: var(--txt);
  }

  /* Subtle floating orbs */
  .bg-orbs{
    position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
  }
  .bg-orbs::before, .bg-orbs::after{
    content:""; position:absolute; filter: blur(60px); opacity:0.35;
    border-radius: 999px; mix-blend-mode: screen; animation: float 18s ease-in-out infinite;
  }
  .bg-orbs::before{ width: 360px; height:360px; background: #6485ff; left:-80px; top: -60px; }
  .bg-orbs::after{ width: 420px; height:420px; background: #a77bff; right:-120px; bottom: -80px; animation-delay: -6s; }
  @keyframes float{ 0%,100%{ transform: translateY(0) } 50%{ transform: translateY(-18px) } }

  /* Canvas */
  .app-shell{ position:relative; z-index:1; }
  .card{
    backdrop-filter: saturate(140%) blur(14px);
    background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.06));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: var(--shadow);
    border-radius: var(--radius-2xl);
  }

  /* Title with shine */
  .brand{
    font-weight: 800; letter-spacing: 0.3px; position: relative; display:inline-block;
    background: linear-gradient(90deg, #b3c7ff, #e5d6ff, #b3c7ff);
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .brand::after{
    content:""; position:absolute; inset:0; background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.6) 35%, transparent 70%);
    transform: translateX(-120%); animation: shine 3.8s ease-in-out infinite;
  }
  @keyframes shine{ 0%{ transform: translateX(-120%)} 60%{ transform: translateX(120%)} 100%{ transform: translateX(120%)} }

  /* Upload button */
  .upload-btn{
    position: relative; overflow: hidden; border-radius: 14px !important; font-weight:700 !important;
    background: linear-gradient(135deg, var(--pri), var(--pri-2)) !important;
    box-shadow: 0 8px 18px rgba(122,162,255,0.28) !important; text-transform:none !important;
  }
  .upload-btn::before{ content:""; position:absolute; inset:0; background: radial-gradient(220px 60px at -20% 20%, rgba(255,255,255,0.35), transparent 40%);
    transform: translateX(-20%); opacity:0.7; }
  .upload-btn:hover{ filter: brightness(1.05); transform: translateY(-1px); }
  .upload-btn:active{ transform: translateY(0px) scale(0.99); }

  /* Mode selector */
  .mode-wrap{ margin-bottom: 18px; }
  .mode-field label{ color: var(--muted) !important; }
  .mode-field .MuiOutlinedInput-notchedOutline{
    border-color: rgba(255,255,255,0.18) !important;
  }
  .mode-field .MuiSelect-select{
    background: rgba(255,255,255,0.06);
  }

  /* Chat panel */
  .chat-paper{ height: 460px; overflow-y: auto; padding: 18px; }
  .chat-paper::-webkit-scrollbar{ width: 10px; }
  .chat-paper::-webkit-scrollbar-thumb{ background: rgba(255,255,255,0.18); border-radius: 8px; }
  .chat-paper::-webkit-scrollbar-track{ background: rgba(255,255,255,0.06); border-radius: 8px; }

  /* Message bubbles */
  .bubble{ position: relative; max-width: 85%; padding: 14px 16px; border-radius: 16px; line-height: 1.5; }
  .from-user .bubble{
    margin-left: auto; background: linear-gradient(180deg, rgba(122,162,255,0.22), rgba(122,162,255,0.12));
    border: 1px solid rgba(122,162,255,0.35);
  }
  .from-bot .bubble{
    background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.06));
    border: 1px solid rgba(255,255,255,0.14);
  }
  .bubble h1,.bubble h2,.bubble h3 { margin: 0 0 8px 0; }
  .bubble p{ margin: 6px 0; color: var(--txt); }
  .bubble code{ background: rgba(0,0,0,0.35); padding: 2px 6px; border-radius: 6px; }

  .author{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); }

  /* Citation chips */
  .citations{ display:flex; flex-wrap:wrap; gap: 6px; margin-top: 10px; }
  .citation-chip{ border:1px solid rgba(122,162,255,0.4) !important; color:#cfe0ff !important; }
  .citation-chip:hover{ background: rgba(122,162,255,0.12) !important; }

  /* Input row */
  .input-row{ display:flex; gap:10px; }
  .input-field .MuiOutlinedInput-notchedOutline{ border-color: rgba(255,255,255,0.16) !important; }
  .input-field input{ color: var(--txt) !important; }
  .send-btn{
    border-radius: 14px !important; color: white !important; font-weight: 700 !important; padding: 0 22px !important; text-transform: none !important;
    background: linear-gradient(135deg, #4ad295, #7aa2ff) !important; box-shadow: 0 8px 20px rgba(74,210,149,0.2) !important;
  }
  .send-btn:hover{ transform: translateY(-1px); filter: brightness(1.05); }
  .send-btn:active{ transform: translateY(0px) scale(0.99); }

  /* Quiz card */
  .quiz-card{ background: linear-gradient(180deg, rgba(74,210,149,0.12), rgba(74,210,149,0.06)); border: 1px solid rgba(74,210,149,0.3); }
  .quiz-answer-ok{ color: var(--ok); font-weight: 700; }
  .quiz-answer-err{ color: var(--err); font-weight: 700; }

  /* Container edge glow */
  .edge-glow{ position: relative; }
  .edge-glow::before{
    content:""; position:absolute; inset:-2px; border-radius: calc(var(--radius-2xl) + 2px);
    background: radial-gradient(600px 160px at 20% -20%, rgba(122,162,255,0.25), transparent 60%),
                radial-gradient(600px 160px at 110% 120%, rgba(167,123,255,0.25), transparent 60%);
    z-index:-1; filter: blur(14px); opacity: 0.9;
  }

  /* Small screens */
  @media (max-width: 520px){
    .chat-paper{ height: 58vh; }
    .bubble{ max-width: 100%; }
  }
`;

function useInjectGlobalCSS() {
  useEffect(() => {
    if (!document.getElementById("nextgen-luxe-css")) {
      const s = document.createElement("style");
      s.id = "nextgen-luxe-css";
      s.innerHTML = STYLES;
      document.head.appendChild(s);
    }
  }, []);
}

// Mode selector component for unique chat modes
function ModeSelector({ mode, setMode }) {
  return (
    <FormControl fullWidth className="mode-wrap mode-field">
      <InputLabel id="mode-select-label">Choose Chat Mode</InputLabel>
      <Select
        labelId="mode-select-label"
        value={mode}
        label="Choose Chat Mode"
        onChange={(e) => setMode(e.target.value)}
        size="small"
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
    <Box className="card quiz-card" sx={{ mt: 2, mb: 3, p: 3 }}>
      {questions.map((q, idx) => (
        <Box key={q.id || idx} mb={3}>
          <Typography variant="subtitle1" component="div" sx={{ fontWeight: 700, mb: 1 }}>
            {idx + 1}. {q.question}
          </Typography>
          <RadioGroup value={answers[q.id] || ""} onChange={(e) => handleChange(q.id, e.target.value)}>
            {q.options.map((opt, i) => (
              <FormControlLabel key={i} value={opt} control={<Radio />} label={opt} disabled={showResults} sx={{ mt: 0.5, mb: 0.5 }} />
            ))}
          </RadioGroup>
          {showResults && (
            <Typography variant="body2" className={answers[q.id] === q.answer ? "quiz-answer-ok" : "quiz-answer-err"} sx={{ mt: 0.5 }}>
              Correct answer: {q.answer}
            </Typography>
          )}
        </Box>
      ))}
      {!showResults && (
        <Button variant="contained" onClick={handleSubmit} size="large" className="send-btn">
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
    <div className="citations">
      {sources.map((src, i) => (
        <Chip key={i} label={src} size="small" className="citation-chip" variant="outlined" onClick={() => window.open(src, "_blank")} />
      ))}
    </div>
  );
}

function App() {
  useInjectGlobalCSS();

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
    if (!msg || !msg.type) {
      return (
        <ListItem key={idx} className="from-bot">
          <div className="bubble"><em>Received invalid response from server.</em></div>
        </ListItem>
      );
    }

    switch (msg.type) {
      case "quiz":
        return <Quiz key={idx} questions={msg.questions} onComplete={(answers) => alert("Quiz submitted!")} />;
      case "text":
      default:
        return (
          <ListItem key={idx} alignItems="flex-start" className={msg.role === "user" ? "from-user" : "from-bot"}>
            <ListItemText
              primary={<span className="author">{msg.role === "user" ? "You" : "Bot"}</span>}
              secondaryTypographyProps={{ component: "div" }}
              secondary={
                <div className="bubble">
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
    <>
      <div className="bg-orbs" />
      <Container maxWidth="sm" className="app-shell edge-glow" sx={{ mt: 6 }}>
        <Box className="card" sx={{ p: { xs: 2.5, sm: 4 } }}>
          <Typography variant="h3" align="center" gutterBottom className="brand">
            NextGenLingo
          </Typography>

          <Button variant="contained" component="label" className="upload-btn" sx={{ mb: 3 }}>
            📂 Upload Document
            <input hidden type="file" onChange={handleFileChange} />
          </Button>

          <ModeSelector mode={chatMode} setMode={setChatMode} />

          <Paper elevation={0} className="card chat-paper">
            <List>
              {chat.map((msg, idx) => (
                <React.Fragment key={idx}>
                  {renderMessage(msg, idx)}
                  {idx < chat.length - 1 && <Divider sx={{ borderColor: "rgba(255,255,255,0.08)" }} />}
                </React.Fragment>
              ))}
              {loading && (
                <ListItem className="from-bot">
                  <div className="bubble"><em>Bot: typing...</em></div>
                </ListItem>
              )}
              <div ref={bottomRef} />
            </List>
          </Paper>

          <Box className="input-row" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Type your question here..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              disabled={loading}
              size="medium"
              className="input-field"
            />
            <Button onClick={sendMessage} variant="contained" disabled={loading || !query.trim()} size="medium" className="send-btn">
              Send
            </Button>
          </Box>
        </Box>
      </Container>
    </>
  );
}

export default App;
