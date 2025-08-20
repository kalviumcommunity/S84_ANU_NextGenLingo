import { Chip, Box } from "@mui/material";

export function CitationChips({ sources }) {
  if (!sources || sources.length === 0) return null;
  return (
    <Box mt={1}>
      {sources.map((src, idx) => (
        <Chip 
          key={idx} 
          label={src} 
          size="small" 
          color="info" 
          sx={{ mr: 1, cursor: "pointer" }}
          onClick={() => window.open(`/documents/${src}`, "_blank")} // adjust to your doc access path
        />
      ))}
    </Box>
  );
}
