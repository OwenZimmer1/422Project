from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.prompts import PromptTemplate
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the Qwen 2.5 Coder 0.5B model and tokenizer
model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"  # Ensure you are using the correct model identifier
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Check if GPU is available and move model to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the LangChain prompt template
multiShot = PromptTemplate(
    input_variables=["method_code"],
    template='''\
Write me a Javadoc comment for the following Java method. Only tell me the Javadoc, **do not return any code.** 

Example 1:
Method:
public String reverseProcessed(String text) {{
    if (text == null) return null;
    String cleaned = text.trim().toLowerCase();
    return new StringBuilder(cleaned).reverse().toString();
}}

Javadoc:
/**
 * Reverses the characters in the given string after trimming whitespace and converting to lowercase.
 *
 * @param text the input string to process
 * @return the reversed, lowercase, trimmed string
 */

Example 2:
Method:
private int add(int a, int b) {{
    return a + b;
}}

Javadoc:
/**
 * Adds two integers.
 *
 * @param a the first integer
 * @param b the second integer
 * @return the sum of the two integers
 */

Now write a Javadoc comment for this method:
Method:
{method_code}
'''
)

# Function to generate the embeddings for each method using the provided prompt
def get_method_embedding(method_code):
    # Format the method using the LangChain template
    formatted_prompt = multiShot.format(method_code=method_code)
    
    # Tokenize and move inputs to GPU
    inputs = tokenizer(formatted_prompt, return_tensors="pt", truncation=True, padding=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}  # Move tensors to GPU

    # Generate outputs and return hidden states by enabling output_hidden_states
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    
    # The hidden states are in the 'hidden_states' field of the output
    # We take the last hidden state and perform mean pooling over the tokens (dim=1)
    last_hidden_state = outputs.hidden_states[-1]  # Get the last layer's hidden states
    return last_hidden_state.mean(dim=1).detach().cpu().numpy()  # Move back to CPU for similarity calculation

# Load methods from the uploaded `allMethods.txt` file
with open(r"C:\Users\eyas1\OneDrive\Desktop\CS 422 Project\422Project\data\allMethodsCombined.json", "r") as file:
    methods = file.read().splitlines()

# Example method from the uploaded file
method_embeddings = [get_method_embedding(method) for method in methods]

# Function to calculate the semantic similarity between a prompt and methods
def evaluate_similarity(prompt_code, methods, method_embeddings):
    prompt_embedding = get_method_embedding(prompt_code)

    similarities = []
    for embedding in method_embeddings:
        similarity = cosine_similarity(prompt_embedding, embedding)[0][0]
        similarities.append(similarity)

    # Calculate statistics
    avg_similarity = np.mean(similarities)
    median_similarity = np.median(similarities)
    min_similarity = np.min(similarities)
    max_similarity = np.max(similarities)
    std_similarity = np.std(similarities)

    # Create the summary dictionary
    summary = {
        "mean": avg_similarity,
        "median": median_similarity,
        "min": min_similarity,
        "max": max_similarity,
        "std": std_similarity
    }

    # Print out the similarities for each method
    for idx, similarity in enumerate(similarities):
        print(f"Similarity with method {idx+1}: {similarity:.4f}")
    
    # Return the summary and detailed similarity info
    return {
        "summary": summary,
        "similarities": similarities
    }

# Example prompt to compare
longmethod2 = '''public BallSeq clone( )
{
    write a javadoc comment for this method
}'''

# Calculate the similarity between the prompt and the methods
results = evaluate_similarity(longmethod2, methods, method_embeddings)

# Output the summary
print("\nSummary of Semantic Similarity Evaluation:")
print(results["summary"])
