from transformers import AutoTokenizer

# Load GPT-2 tokenizer (commonly used)
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def get_tokens(text):
    """Return list of tokens for the input text."""
    return tokenizer.tokenize(text)

def count_tokens(text):
    """Return number of tokens for the input text."""
    return len(tokenizer.encode(text))

if __name__ == "__main__":
    sample_text = "Python is a programming language and html is a markup language"
    print("Text:", sample_text)
    print("Tokens:", get_tokens(sample_text))
    print("Number of tokens:", count_tokens(sample_text))
