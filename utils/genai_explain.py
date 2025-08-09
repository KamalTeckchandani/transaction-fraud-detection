import openai

# Set this to your OpenAI API key before running
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_explanation(transaction, reasons):
    prompt = f"Explain briefly why this transaction may be fraudulent: reasons - {reasons}, transaction details - {transaction}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    explanation = response['choices'][0]['message']['content']
    return explanation

if __name__ == "__main__":
    example_tx = {"amount": 4000, "location": "Russia"}
    example_reasons = ["High amount", "From restricted location"]
    print(generate_explanation(example_tx, example_reasons))
