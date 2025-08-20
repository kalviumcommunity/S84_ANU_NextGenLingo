import React, { useState } from "react";
import { Box, Typography, RadioGroup, FormControlLabel, Radio, Button } from "@mui/material";

export function Quiz({ questions, onComplete }) {
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  const handleChange = (qid, ans) => {
    setAnswers(prev => ({ ...prev, [qid]: ans }));
  };

  const handleSubmit = () => {
    setShowResults(true);
    // You can compute score here or pass answers to parent
    if(onComplete) onComplete(answers);
  };

  return (
    <Box>
      {questions.map((q, idx) => (
        <Box key={idx} mb={2}>
          <Typography variant="subtitle1">{`${idx + 1}. ${q.question}`}</Typography>
          <RadioGroup value={answers[q.id] || ""} onChange={(e) => handleChange(q.id, e.target.value)}>
            {q.options.map((opt, i) => (
              <FormControlLabel key={i} value={opt} control={<Radio />} label={opt} disabled={showResults} />
            ))}
          </RadioGroup>
          {showResults && (
            <Typography variant="body2" color={answers[q.id] === q.answer ? "green" : "error"}>
              Correct answer: {q.answer}
            </Typography>
          )}
        </Box>
      ))}

      {!showResults && (
        <Button variant="contained" onClick={handleSubmit} disabled={Object.keys(answers).length < questions.length}>
          Submit Answers
        </Button>
      )}
    </Box>
  );
}
