# 🎛️ LLM Technical Parameters Explained

## Your Questions Answered:
1. **Temperature** - Controls randomness/creativity in responses
2. **Vector Embeddings** - How text is converted to numbers
3. **Tokenization** - How text is split into processable units

---

## 1️⃣ TEMPERATURE (Context Boundary Control)

### **What is Temperature?**

Temperature is a **hyperparameter** that controls the **randomness** and **creativity** of LLM responses.

Think of it like this:
- **Low temperature** = Conservative, predictable, focused (like a precise calculator)
- **High temperature** = Creative, random, diverse (like a creative artist)

---

### **Temperature Scale:**

```
0.0  ─────────────── 0.7 ─────────────── 1.0 ─────────────── 2.0
│                      │                    │                   │
Deterministic      Balanced           Creative           Chaotic
(same answer)      (best for         (varied)          (random)
                    most tasks)
```

---

### **How It Works Mathematically:**

When an LLM generates text, it predicts the next word/token based on **probabilities**:

```python
# Without temperature (raw probabilities)
Next word predictions:
"The weather is ___"
- "sunny": 60%
- "cloudy": 30%
- "rainy": 10%

# With Temperature = 0.1 (LOW - More Focused)
Probabilities become MORE extreme:
- "sunny": 85%  ← Amplified
- "cloudy": 13%
- "rainy": 2%   ← Suppressed

# With Temperature = 1.0 (MEDIUM - Balanced)
Probabilities stay the same:
- "sunny": 60%
- "cloudy": 30%
- "rainy": 10%

# With Temperature = 2.0 (HIGH - More Random)
Probabilities become FLATTER:
- "sunny": 45%  ← Reduced
- "cloudy": 35%
- "rainy": 20%  ← Increased
```

**Formula:**
```python
probability_i = exp(logit_i / temperature) / sum(exp(logit_j / temperature))
```

---

### **Temperature in Your WalSmart Project:**

Let me check what temperature you're currently using:

```python
# In your ai-service/main.py
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=messages,
    # ⚠️ NO temperature parameter specified!
    # Default is usually 1.0
)
```

**You're NOT setting temperature**, so it defaults to **~1.0** (balanced).

---

### **Recommended Temperature Settings for Your Features:**

| Feature | Recommended Temp | Reason |
|---------|-----------------|---------|
| **Product Q&A** | `0.2 - 0.4` | Need consistent, accurate answers |
| **Intent Detection** | `0.1 - 0.2` | Classification needs to be precise |
| **AI Search** | `0.3 - 0.5` | Want consistent product matching |
| **Sentiment Analysis** | `0.2 - 0.3` | Sentiment should be consistent |
| **Recipe Generation** | `0.7 - 1.0` | Can be more creative with recipes |
| **Recommendations** | `0.5 - 0.7` | Some variety is good |
| **Follow-up Questions** | `0.8 - 1.2` | Want diverse suggestions |

---

### **Example: Temperature Impact on Product Q&A**

**Question:** "How do I cook this rice?"

**Temperature = 0.2 (Low):**
```
Every time: "To cook Basmati rice, rinse 1 cup rice thoroughly, 
add 2 cups water, bring to boil, reduce heat, simmer covered for 
15 minutes, let rest 5 minutes, fluff and serve."
```

**Temperature = 1.5 (High):**
```
Try 1: "Rinse the rice and cook with water in a 1:2 ratio for about 15 mins!"
Try 2: "Want perfectly fluffy rice? Start by washing it well..."
Try 3: "Here's a pro tip: soak your rice for 30 minutes first..."
```

---

### **How to Add Temperature to Your Code:**

```python
# ai-service/main.py - Product Q&A
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=messages,
    temperature=0.3,  # ← ADD THIS for consistent answers
    max_tokens=500,   # Optional: limit response length
)

# For Intent Detection (needs to be very precise)
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=messages,
    temperature=0.1,  # ← Very low for classification
)

# For Recipe Generation (can be creative)
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=messages,
    temperature=0.8,  # ← Higher for creative recipes
)
```

---

## 2️⃣ VECTOR EMBEDDINGS (Text → Numbers)

### **What are Vector Embeddings?**

Embeddings are **dense numerical representations** of text that capture semantic meaning.

Think of it as GPS coordinates for words in "meaning space":
- Similar words have nearby coordinates
- Different words are far apart

---

### **Visual Example:**

```
3D Meaning Space:
                    ↑ (Royalty dimension)
                    │
           "queen" ●│     ● "king"
                    │
            "woman" ●│     ● "man"
                    │
           ─────────┼──────────→ (Gender dimension)
                    │
                    ↓
```

Mathematical representation:
```python
"king"   = [0.8, 0.6, 0.9, ...] (768 dimensions for BERT)
"queen"  = [0.8, -0.6, 0.9, ...] 
"man"    = [0.1, 0.6, 0.2, ...]
"woman"  = [0.1, -0.6, 0.2, ...]

# Famous example:
king - man + woman ≈ queen
[0.8, 0.6, 0.9] - [0.1, 0.6, 0.2] + [0.1, -0.6, 0.2] ≈ [0.8, -0.6, 0.9]
```

---

### **What Models Create Embeddings?**

#### **For GPT/OpenAI Models:**

OpenAI uses **their own embedding models**:

```python
# You can get embeddings explicitly
from openai import OpenAI

client = OpenAI(api_key="your-key")

# Create embeddings
response = client.embeddings.create(
    model="text-embedding-ada-002",  # OpenAI's embedding model
    input="I want to make sushi"
)

embedding = response.data[0].embedding
# Returns: List of 1536 floats
# [0.012, -0.034, 0.156, ..., -0.023]
```

**OpenAI Embedding Models:**
- `text-embedding-ada-002` - 1536 dimensions, $0.0001 per 1K tokens
- `text-embedding-3-small` - 1536 dimensions, newer, cheaper
- `text-embedding-3-large` - 3072 dimensions, highest quality

#### **For Gemini Models:**

Google uses **embeddings from the Transformer architecture**:

```python
# Gemini creates embeddings internally
# You typically don't access them directly
# They're part of the model's attention mechanism
```

#### **In Your WalSmart Project:**

**You're NOT explicitly using embeddings**, but they're happening **internally**:

```
Your text: "I want sushi"
    ↓
LLM tokenizes it → [token_1, token_2, token_3]
    ↓
LLM creates embeddings internally → [[0.1, 0.5, ...], [0.3, 0.2, ...], ...]
    ↓
LLM processes through transformer layers
    ↓
LLM generates response
```

---

### **Common Embedding Models (If You Want to Use Them):**

| Model | Dimensions | Use Case | Library |
|-------|-----------|----------|---------|
| **Word2Vec** | 100-300 | Classic word embeddings | gensim |
| **GloVe** | 50-300 | Stanford's word vectors | gensim |
| **FastText** | 300 | Facebook, handles typos | gensim |
| **BERT** | 768 | Contextual embeddings | transformers |
| **Sentence-BERT** | 384-768 | Sentence similarity | sentence-transformers |
| **OpenAI Ada** | 1536 | Best for semantic search | openai |

---

### **When to Use Embeddings Explicitly:**

You'd use embeddings for:

1. **Semantic Search** (find similar products)
2. **Clustering** (group similar items)
3. **Recommendation** (find similar products)
4. **Duplicate Detection** (find similar queries)

**Example - Semantic Product Search:**

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Create embeddings for all products (one-time)
product_embeddings = {}
for product in products:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=f"{product['name']} {product['description']}"
    )
    product_embeddings[product['id']] = response.data[0].embedding

# 2. Search by embedding similarity
query = "protein-rich food"
query_embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input=query
).data[0].embedding

# 3. Find most similar products
from sklearn.metrics.pairwise import cosine_similarity

similarities = {}
for product_id, emb in product_embeddings.items():
    similarity = cosine_similarity([query_embedding], [emb])[0][0]
    similarities[product_id] = similarity

# Top 5 most similar
top_products = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:5]
```

---

## 3️⃣ TOKENIZATION (Text → Tokens)

### **What is Tokenization?**

Tokenization is the process of **breaking text into smaller units** (tokens) that the model can process.

Think of it like breaking a sentence into LEGO blocks.

---

### **Why is Tokenization Needed?**

LLMs don't understand words directly. They understand **tokens** (numbers).

```
Text → Tokens → Token IDs → Embeddings → Processing
```

---

### **Different Tokenization Methods:**

#### **1. Word-Level Tokenization (Simple)**

```python
text = "I want to make sushi"
tokens = text.split(" ")
# ["I", "want", "to", "make", "sushi"]
```

**Problem:** 
- Large vocabulary (millions of words)
- Can't handle typos or new words
- "running" and "run" are different tokens

---

#### **2. Character-Level Tokenization**

```python
text = "sushi"
tokens = list(text)
# ["s", "u", "s", "h", "i"]
```

**Problem:**
- Too many tokens for long text
- Loses word meaning

---

#### **3. Subword Tokenization (What LLMs Use)**

**This is what GPT and Gemini use!**

Breaks words into **meaningful subword units**:

```python
text = "unbelievable"
tokens = ["un", "believ", "able"]

text = "tokenization"
tokens = ["token", "ization"]
```

**Advantages:**
- ✅ Handles new words
- ✅ Smaller vocabulary
- ✅ Captures morphology (word structure)
- ✅ Handles typos better

---

### **Tokenization Algorithms Used by LLMs:**

#### **A. BPE (Byte Pair Encoding) - Used by GPT**

**How it works:**
1. Start with characters
2. Find most frequent pair
3. Merge them into a new token
4. Repeat

```python
Iteration 1: "sushi rice" → ["s", "u", "s", "h", "i", " ", "r", "i", "c", "e"]
Most frequent pair: "s" + "u" = "su"

Iteration 2: ["su", "s", "h", "i", " ", "r", "i", "c", "e"]
Most frequent pair: "su" + "s" = "sus"

Final: ["sus", "hi", " ", "ri", "ce"]
```

**Used by:**
- GPT-2, GPT-3, GPT-4
- RoBERTa
- BART

---

#### **B. WordPiece - Used by BERT**

Similar to BPE but uses **likelihood** instead of frequency:

```python
"tokenization" → ["token", "##ization"]
```

The `##` indicates a subword continuation.

**Used by:**
- BERT
- DistilBERT
- ELECTRA

---

#### **C. SentencePiece - Used by Gemini/T5**

Language-agnostic tokenization (works for any language):

```python
text = "I want sushi"
tokens = ["▁I", "▁want", "▁su", "shi"]
```

The `▁` indicates word boundaries.

**Used by:**
- T5
- ALBERT
- Google Gemini
- LLaMA

---

#### **D. Tiktoken - Used by GPT-4**

OpenAI's optimized tokenizer for GPT models:

```python
import tiktoken

# For GPT-4o-mini
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

text = "I want to make sushi at home"
tokens = encoding.encode(text)
print(tokens)
# [40, 1390, 311, 1304, 67322, 520, 2162]

# Decode back
text_back = encoding.decode(tokens)
print(text_back)
# "I want to make sushi at home"
```

---

### **Tokenization in Your WalSmart Project:**

**For OpenAI (GPT-4o-mini):**

```python
# Your current code
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=messages,
)

# What happens internally:
# 1. Your text is tokenized using Tiktoken
# 2. Tokens are converted to IDs
# 3. IDs are embedded into vectors
# 4. Processed through transformer
# 5. Output tokens generated
# 6. Decoded back to text
```

**For Gemini:**

```python
# Your Genkit code
const ai = genkit({
  plugins: [googleAI()],
  model: 'googleai/gemini-2.0-flash',
});

// Internally uses SentencePiece tokenizer
// You don't see it, but it's happening
```

---

### **Token Limits (Context Window):**

Each model has a **maximum token limit**:

| Model | Max Tokens | Context Window |
|-------|-----------|----------------|
| **GPT-4o-mini** | 128,000 | Input + Output |
| **GPT-4** | 8,192 - 32,768 | Depends on version |
| **Gemini 2.0 Flash** | 1,048,576 (1M) | Huge! |
| **GPT-3.5-turbo** | 16,385 | Input + Output |

---

### **How to Count Tokens:**

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens for GPT models"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example
text = "I want to make sushi at home"
token_count = count_tokens(text)
print(f"Token count: {token_count}")  # Output: 8 tokens

# For pricing
COST_PER_1K_TOKENS = 0.0001  # GPT-4o-mini input
total_cost = (token_count / 1000) * COST_PER_1K_TOKENS
print(f"Cost: ${total_cost}")
```

---

### **Why Tokenization Matters:**

1. **Pricing** - You pay per token, not per word
2. **Context Limits** - Can't exceed max tokens
3. **Performance** - More tokens = slower response
4. **Prompt Engineering** - Need to fit within limits

---

## 🎯 Summary Table

| Parameter | What It Does | Where Used | Your Project |
|-----------|-------------|------------|--------------|
| **Temperature** | Controls randomness (0.0-2.0) | Response generation | Not set (defaults to 1.0) |
| **Embeddings** | Text → Vector numbers | Internal to LLM | GPT uses internal embeddings |
| **Tokenization** | Text → Token IDs | Pre-processing | BPE (GPT), SentencePiece (Gemini) |

---

## 🛠️ Recommendations for Your Project:

### **1. Add Temperature Control:**

```python
# ai-service/main.py
TEMPERATURE_CONFIG = {
    "product_qa": 0.3,        # Consistent answers
    "intent_detection": 0.1,   # Precise classification
    "recipe_details": 0.8,     # Creative recipes
    "recommendations": 0.6,    # Some variety
}

# Use in code:
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=messages,
    temperature=TEMPERATURE_CONFIG["product_qa"],  # ← Add this
)
```

### **2. Monitor Token Usage:**

```python
# Track tokens for cost monitoring
resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=messages,
    temperature=0.3,
)

# Check usage
print(f"Input tokens: {resp.usage.prompt_tokens}")
print(f"Output tokens: {resp.usage.completion_tokens}")
print(f"Total tokens: {resp.usage.total_tokens}")
```

### **3. Consider Explicit Embeddings (Optional):**

For semantic product search:

```python
# Create product embeddings database
# Then search by similarity instead of LLM calls
# This is FASTER and CHEAPER for simple searches
```

---

## 📚 Further Reading:

- **Temperature:** OpenAI API docs on sampling parameters
- **Embeddings:** Sentence Transformers documentation
- **Tokenization:** Hugging Face tokenizers guide

---

**Need more details on any of these?** Let me know!
