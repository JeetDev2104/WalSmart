"""
Practical Examples: Temperature, Embeddings, and Tokenization
==============================================================

This file demonstrates how to use these parameters in your WalSmart project.
"""

import os
from typing import List, Dict, Any
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# 1. TEMPERATURE EXAMPLES
# ============================================================================

def demonstrate_temperature():
    """Show how temperature affects responses"""
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_AI_API_KEY")
    )
    
    prompt = "How do I cook Basmati rice?"
    
    print("=" * 80)
    print("TEMPERATURE DEMONSTRATION")
    print("=" * 80)
    
    temperatures = [0.1, 0.7, 1.5]
    
    for temp in temperatures:
        print(f"\n{'='*80}")
        print(f"Temperature: {temp}")
        print(f"{'='*80}")
        
        # Ask the same question 3 times
        for trial in range(1, 4):
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temp,
                max_tokens=100  # Limit for demo
            )
            
            answer = response.choices[0].message.content
            print(f"\nTrial {trial}:")
            print(f"  {answer[:100]}...")  # Show first 100 chars


def recommended_temperatures_for_walSmart():
    """
    Recommended temperature settings for different WalSmart features
    """
    
    return {
        # Very precise tasks
        "intent_detection": 0.1,       # Need exact classification
        "sentiment_analysis": 0.2,      # Consistent sentiment scoring
        
        # Moderately precise tasks
        "product_qa": 0.3,              # Consistent but natural answers
        "ai_search": 0.4,               # Some variety in search results
        
        # Balanced tasks
        "recommendations": 0.6,         # Variety in recommendations
        "general_chat": 0.7,            # Natural conversation
        
        # Creative tasks
        "recipe_generation": 0.8,       # Creative recipe ideas
        "meal_planning": 0.9,           # Diverse meal suggestions
        "follow_up_questions": 1.0,     # Diverse question generation
    }


# ============================================================================
# 2. TOKENIZATION EXAMPLES
# ============================================================================

def count_tokens_example():
    """Demonstrate token counting for cost estimation"""
    
    print("\n" + "=" * 80)
    print("TOKENIZATION DEMONSTRATION")
    print("=" * 80)
    
    # Get the tokenizer for GPT-4o-mini
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    examples = [
        "sushi",
        "I want to make sushi",
        "I want to make sushi at home with fresh ingredients",
        "How do I cook Basmati rice perfectly every time?",
    ]
    
    for text in examples:
        # Encode to tokens
        tokens = encoding.encode(text)
        
        # Decode back to see token strings
        token_strings = [encoding.decode([token]) for token in tokens]
        
        print(f"\nText: '{text}'")
        print(f"Token count: {len(tokens)}")
        print(f"Token IDs: {tokens}")
        print(f"Token strings: {token_strings}")


def estimate_api_cost():
    """Calculate API costs based on token usage"""
    
    # Pricing for GPT-4o-mini (as of 2024)
    PRICING = {
        "gpt-4o-mini": {
            "input": 0.150 / 1_000_000,   # $0.150 per 1M input tokens
            "output": 0.600 / 1_000_000,  # $0.600 per 1M output tokens
        }
    }
    
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    # Example: Product Q&A request
    prompt = """You are a helpful shopping assistant.
    Product: Basmati Rice Premium Grade
    Description: High-quality aged basmati rice
    Price: $12.99
    
    User Question: How do I cook this rice?
    
    Answer the user's question."""
    
    input_tokens = len(encoding.encode(prompt))
    expected_output_tokens = 150  # Estimated
    
    input_cost = input_tokens * PRICING["gpt-4o-mini"]["input"]
    output_cost = expected_output_tokens * PRICING["gpt-4o-mini"]["output"]
    total_cost = input_cost + output_cost
    
    print("\n" + "=" * 80)
    print("API COST ESTIMATION")
    print("=" * 80)
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {expected_output_tokens} (estimated)")
    print(f"Input cost: ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost per request: ${total_cost:.6f}")
    print(f"\nCost for 1,000 requests: ${total_cost * 1000:.2f}")
    print(f"Cost for 10,000 requests: ${total_cost * 10000:.2f}")


# ============================================================================
# 3. VECTOR EMBEDDINGS EXAMPLES
# ============================================================================

def create_embeddings_example():
    """Demonstrate creating and using embeddings"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("\n" + "=" * 80)
    print("VECTOR EMBEDDINGS DEMONSTRATION")
    print("=" * 80)
    
    # Create embeddings for products
    products = [
        "Fresh Chicken Breast",
        "Basmati Rice Premium Grade",
        "Organic Baby Spinach",
        "Wild Caught Salmon Fillet",
    ]
    
    print("\nCreating embeddings for products...")
    embeddings = {}
    
    for product in products:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=product
        )
        embeddings[product] = response.data[0].embedding
        
        print(f"✓ {product}")
        print(f"  Embedding size: {len(embeddings[product])} dimensions")
        print(f"  First 5 values: {embeddings[product][:5]}")
    
    # Calculate similarity between products
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    print("\n" + "=" * 80)
    print("SIMILARITY SCORES")
    print("=" * 80)
    
    # Convert to numpy array
    product_names = list(embeddings.keys())
    embedding_matrix = np.array([embeddings[p] for p in product_names])
    
    # Calculate similarity matrix
    similarities = cosine_similarity(embedding_matrix)
    
    # Print similarity scores
    for i, product1 in enumerate(product_names):
        print(f"\n{product1}:")
        for j, product2 in enumerate(product_names):
            if i != j:  # Skip self-similarity
                score = similarities[i][j]
                print(f"  vs {product2}: {score:.3f}")


def semantic_search_example():
    """Demonstrate semantic search using embeddings"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("\n" + "=" * 80)
    print("SEMANTIC SEARCH EXAMPLE")
    print("=" * 80)
    
    # Product database
    products = [
        {"name": "Fresh Chicken Breast", "category": "Meat"},
        {"name": "Wild Salmon Fillet", "category": "Seafood"},
        {"name": "Basmati Rice", "category": "Grains"},
        {"name": "Quinoa", "category": "Grains"},
        {"name": "Tofu Block", "category": "Protein"},
        {"name": "Greek Yogurt", "category": "Dairy"},
    ]
    
    # Create embeddings for all products
    print("Building product embedding database...")
    product_embeddings = {}
    for product in products:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=f"{product['name']} {product['category']}"
        )
        product_embeddings[product['name']] = response.data[0].embedding
    
    # Search query
    query = "high protein food"
    print(f"\nSearch query: '{query}'")
    
    # Create query embedding
    query_response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    )
    query_embedding = query_response.data[0].embedding
    
    # Calculate similarities
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    similarities = {}
    for product_name, product_emb in product_embeddings.items():
        similarity = cosine_similarity(
            [query_embedding], 
            [product_emb]
        )[0][0]
        similarities[product_name] = similarity
    
    # Sort by similarity
    ranked = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    
    print("\nSearch Results (ranked by relevance):")
    for i, (product, score) in enumerate(ranked, 1):
        print(f"{i}. {product} (score: {score:.3f})")


# ============================================================================
# 4. PRACTICAL IMPLEMENTATION FOR WALSMART
# ============================================================================

def improved_product_qa_with_temperature(
    product: Dict[str, Any],
    question: str,
    api_key: str
) -> Dict[str, Any]:
    """
    Enhanced Product Q&A with temperature control
    """
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    prompt = f"""You are a helpful shopping assistant.
Product: {product['name']}
Description: {product.get('description', '')}
Price: ${product.get('price', 0)}

User Question: {question}

Answer the user's question concisely."""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # Low temperature for consistent answers
        max_tokens=200,
    )
    
    return {
        "answer": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens,
        "cost": calculate_cost(response.usage),
    }


def calculate_cost(usage) -> float:
    """Calculate API cost from usage"""
    PRICING = {
        "input": 0.150 / 1_000_000,
        "output": 0.600 / 1_000_000,
    }
    
    input_cost = usage.prompt_tokens * PRICING["input"]
    output_cost = usage.completion_tokens * PRICING["output"]
    
    return input_cost + output_cost


def token_aware_prompt_builder(
    base_prompt: str,
    context: str,
    max_tokens: int = 4000
) -> str:
    """
    Build a prompt that stays within token limits
    """
    
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    # Count base prompt tokens
    base_tokens = len(encoding.encode(base_prompt))
    
    # Calculate available tokens for context
    available_tokens = max_tokens - base_tokens - 100  # Reserve 100 for safety
    
    # Truncate context if needed
    context_tokens = encoding.encode(context)
    if len(context_tokens) > available_tokens:
        # Truncate and decode back
        context_tokens = context_tokens[:available_tokens]
        context = encoding.decode(context_tokens)
        print(f"⚠️ Context truncated to fit token limit")
    
    return f"{base_prompt}\n\nContext: {context}"


# ============================================================================
# MAIN - RUN ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TECHNICAL PARAMETERS DEMONSTRATION")
    print("=" * 80)
    
    # Check for API keys
    if not os.getenv("OPEN_AI_API_KEY"):
        print("⚠️ OPEN_AI_API_KEY not found. Some examples will be skipped.")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEY not found. Embedding examples will be skipped.")
    
    # 1. Temperature
    print("\n" + "=" * 80)
    print("RECOMMENDED TEMPERATURES FOR WALSMART")
    print("=" * 80)
    temps = recommended_temperatures_for_walSmart()
    for feature, temp in temps.items():
        print(f"{feature:25s}: {temp}")
    
    # Uncomment to run live demos (requires API keys)
    # demonstrate_temperature()
    
    # 2. Tokenization
    count_tokens_example()
    estimate_api_cost()
    
    # 3. Embeddings
    # Uncomment to run live demos (requires OpenAI API key)
    # create_embeddings_example()
    # semantic_search_example()
    
    print("\n" + "=" * 80)
    print("✅ Examples completed!")
    print("=" * 80)
    print("\nTo run live API examples, uncomment the function calls in main()")
    print("Make sure you have OPEN_AI_API_KEY and OPENAI_API_KEY set in .env")
