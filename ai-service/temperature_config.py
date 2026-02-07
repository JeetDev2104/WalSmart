# Temperature Configuration for WalSmart AI Service
# ==================================================
# Add this to your ai-service/main.py

"""
TEMPERATURE SETTINGS GUIDE
---------------------------

Temperature controls the randomness of LLM responses:
- 0.0 - 0.3: Deterministic, consistent (best for classification, Q&A)
- 0.4 - 0.7: Balanced (general purpose)
- 0.8 - 1.2: Creative (for recipes, suggestions)
- 1.3 - 2.0: Very random (usually too unpredictable)

For WalSmart features:
"""

# Temperature configuration for each endpoint
TEMPERATURE_CONFIG = {
    # Precise tasks - need consistent classification
    "intent_detection": 0.1,        # Must classify correctly every time
    "analyze_review": 0.2,          # Sentiment should be consistent
    
    # Moderately precise - need accurate but natural responses
    "product_qa": 0.3,              # Consistent product answers
    "ai_search": 0.4,               # Consistent product matching
    
    # Balanced - can have some variation
    "recommendations": 0.6,         # Some variety in suggestions
    
    # Creative - want diverse outputs
    "recipe_details": 0.8,          # Creative recipe ideas
    "follow_up_questions": 1.0,     # Diverse question generation
}

# Token limits for cost control
MAX_TOKENS = {
    "product_qa": 500,
    "analyze_review": 200,
    "ai_search": 100,
    "recommendations": 150,
    "intent_detection": 150,
    "recipe_details": 800,
}

# Example: Update your product_qa endpoint
"""
@app.post("/product-qa", response_model=ProductQAResponse)
async def product_qa(request: ProductQARequest):
    try:
        # ... existing code ...
        
        resp = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages,
            
            # ADD THESE PARAMETERS:
            temperature=TEMPERATURE_CONFIG["product_qa"],  # ← Consistent answers
            max_tokens=MAX_TOKENS["product_qa"],           # ← Cost control
        )
        
        # Log token usage for monitoring
        print(f"Tokens used: {resp.usage.total_tokens} "
              f"(input: {resp.usage.prompt_tokens}, "
              f"output: {resp.usage.completion_tokens})")
        
        # ... rest of existing code ...
"""

# Cost calculation helper
def calculate_request_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate cost for a single request
    
    GPT-4o-mini pricing (as of 2024):
    - Input: $0.150 per 1M tokens
    - Output: $0.600 per 1M tokens
    """
    PRICING = {
        "input": 0.150 / 1_000_000,
        "output": 0.600 / 1_000_000,
    }
    
    input_cost = prompt_tokens * PRICING["input"]
    output_cost = completion_tokens * PRICING["output"]
    
    return input_cost + output_cost


# Example usage in your endpoints
"""
# After getting response
cost = calculate_request_cost(
    resp.usage.prompt_tokens,
    resp.usage.completion_tokens
)
print(f"Request cost: ${cost:.6f}")
"""

# Recommended updates for each endpoint:

ENDPOINT_UPDATES = """
1. /product-qa
   - temperature: 0.3 (consistent answers)
   - max_tokens: 500
   - Why: Users expect same answer to same question

2. /analyze-review
   - temperature: 0.2 (consistent sentiment)
   - max_tokens: 200
   - Why: Sentiment analysis should be stable

3. /ai-search
   - temperature: 0.4 (mostly consistent)
   - max_tokens: 100
   - Why: Product matching should be reliable

4. /recommend
   - temperature: 0.6 (some variety)
   - max_tokens: 150
   - Why: Users appreciate diverse recommendations

5. /detect-intent
   - temperature: 0.1 (very precise)
   - max_tokens: 150
   - Why: Classification must be accurate

6. /recipe-details
   - temperature: 0.8 (creative)
   - max_tokens: 800
   - Why: Recipes can be creative and varied
"""

print(ENDPOINT_UPDATES)
