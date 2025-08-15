from prompting import zero_shot_prompt

EVAL_DATASET = [
    {"question": "What is the capital of Japan?", "expected": "Tokyo"},
    {"question": "What is the capital of Italy?", "expected": "Rome"},
    {"question": "Who wrote Hamlet?", "expected": "Shakespeare"},
    {"question": "What is the boiling point of water (Celsius)?", "expected": "100"},
    {"question": "What language is spoken in Brazil?", "expected": "Portuguese"},
]

def judge_answer(expected, output):
    prompt = (
        f"Expected answer: {expected}\n"
        f"Model output: {output}\n"
        "Is the output semantically and factually equivalent to the expected answer? "
        "Reply only 'Yes' or 'No'."
    )
    judge_result = zero_shot_prompt(prompt)
    return "yes" in judge_result.lower()

def evaluate():
    results = []
    for item in EVAL_DATASET:
        output = zero_shot_prompt(item['question'])
        correct = judge_answer(item['expected'], output)
        results.append({
            "question": item["question"],
            "expected": item["expected"],
            "output": output,
            "correct": correct
        })
    return results

if __name__ == "__main__":
    results = evaluate()
    for r in results:
        print(f"Q: {r['question']}")
        print(f"Expected: {r['expected']}")
        print(f"Output:   {r['output']}")
        print(f"Correct:  {r['correct']}\n")
