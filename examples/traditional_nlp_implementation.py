"""
Traditional NLP Implementation Examples
========================================

This file shows how to implement WalSmart's AI features WITHOUT using LLMs.
Instead, we use classical NLP algorithms and machine learning.

Requirements:
pip install nltk spacy scikit-learn fuzzywuzzy textblob surprise mlxtend
python -m spacy download en_core_web_sm
"""

import re
import json
from typing import List, Dict, Any, Tuple
from collections import Counter

# Core NLP libraries
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

# Fuzzy matching
from fuzzywuzzy import fuzz, process

# Recommendation algorithms
from surprise import SVD, Dataset, Reader
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Sentiment
from textblob import TextBlob

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')


# ============================================================================
# FEATURE 1: AI SEARCH & INTENT DETECTION
# ============================================================================

class IntentDetector:
    """
    Detects user intent without using LLMs.
    Uses Naive Bayes classification with TF-IDF features.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.classifier = MultinomialNB()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.is_trained = False
    
    def preprocess(self, text: str) -> str:
        """Preprocess text: lowercase, lemmatize, remove stopwords"""
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token.isalpha() and token not in self.stop_words
        ]
        
        return ' '.join(tokens)
    
    def train(self, training_data: List[Tuple[str, str]]):
        """
        Train the intent classifier.
        
        Args:
            training_data: List of (query, intent) tuples
            
        Example:
            [
                ("I want to make sushi", "recipe"),
                ("buy chicken breast", "product"),
                ("best moisturizer for dry skin", "skincare"),
                ("show me running shoes", "product"),
            ]
        """
        queries, intents = zip(*training_data)
        
        # Preprocess
        processed_queries = [self.preprocess(q) for q in queries]
        
        # Vectorize
        X = self.vectorizer.fit_transform(processed_queries)
        
        # Train
        self.classifier.fit(X, intents)
        self.is_trained = True
        
        print(f"✅ Intent detector trained on {len(training_data)} examples")
    
    def predict(self, query: str) -> Tuple[str, float]:
        """Predict intent with confidence score"""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        processed = self.preprocess(query)
        X = self.vectorizer.transform([processed])
        
        intent = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = max(probabilities)
        
        return intent, confidence


class EntityExtractor:
    """Extract entities (products, ingredients, categories) from queries"""
    
    def __init__(self):
        self.nlp = nlp
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords using POS tagging"""
        doc = self.nlp(text)
        
        keywords = []
        
        # Extract nouns and proper nouns
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
                keywords.append(token.lemma_.lower())
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG', 'GPE', 'FOOD']:
                keywords.append(ent.text.lower())
        
        return list(set(keywords))
    
    def extract_ingredients(self, text: str, available_products: List[str]) -> List[str]:
        """Match extracted keywords to available products using fuzzy matching"""
        keywords = self.extract_keywords(text)
        
        matched_products = []
        
        for keyword in keywords:
            # Fuzzy match against product list
            matches = process.extract(keyword, available_products, limit=3, scorer=fuzz.token_sort_ratio)
            
            # Add matches with similarity > 60%
            for match, score in matches:
                if score > 60 and match not in matched_products:
                    matched_products.append(match)
        
        return matched_products


class TraditionalAISearch:
    """Complete AI search system without LLMs"""
    
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()
    
    def train(self, training_data: List[Tuple[str, str]]):
        """Train the intent detector"""
        self.intent_detector.train(training_data)
    
    def search(self, query: str, available_products: List[str]) -> Dict[str, Any]:
        """
        Perform AI-powered search without LLMs
        
        Returns:
            {
                "type": "recipe|product|skincare|etc",
                "keywords": ["keyword1", "keyword2"],
                "ingredients": ["Product 1", "Product 2"],
                "confidence": 0.85
            }
        """
        # Detect intent
        intent, confidence = self.intent_detector.predict(query)
        
        # Extract keywords
        keywords = self.entity_extractor.extract_keywords(query)
        
        # Match products
        ingredients = self.entity_extractor.extract_ingredients(query, available_products)
        
        return {
            "type": intent,
            "keywords": keywords,
            "ingredients": ingredients,
            "confidence": confidence,
            "category": self._map_intent_to_category(intent)
        }
    
    def _map_intent_to_category(self, intent: str) -> str:
        """Map intent to product category"""
        mapping = {
            "recipe": "Groceries",
            "skincare": "Skincare",
            "clothing": "Clothing",
            "electronics": "Electronics",
            "product": "General"
        }
        return mapping.get(intent, "General")


# ============================================================================
# FEATURE 2: SENTIMENT ANALYSIS
# ============================================================================

class SentimentAnalyzer:
    """Analyze product review sentiment without LLMs"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_review(self, review_text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
        
        Returns:
            {
                "positive": 75,
                "negative": 25,
                "aspects": {
                    "quality": 85,
                    "price": 30,
                    "service": 70
                }
            }
        """
        # Overall sentiment using VADER
        vader_scores = self.vader.polarity_scores(review_text)
        
        # Map compound score (-1 to 1) to positive/negative percentages
        compound = vader_scores['compound']
        
        if compound >= 0:
            positive = int((compound + 1) * 50)  # Scale to 50-100
            negative = 100 - positive
        else:
            negative = int((abs(compound) + 1) * 50)  # Scale to 50-100
            positive = 100 - negative
        
        # Aspect-based sentiment analysis
        aspects = self._aspect_based_sentiment(review_text)
        
        return {
            "positive": positive,
            "negative": negative,
            "aspects": aspects
        }
    
    def _aspect_based_sentiment(self, text: str) -> Dict[str, int]:
        """Extract sentiment for specific aspects"""
        aspects = {
            "quality": ["quality", "good", "great", "excellent", "poor", "bad", "terrible"],
            "price": ["price", "expensive", "cheap", "cost", "value", "affordable"],
            "service": ["service", "delivery", "shipping", "fast", "slow"],
            "durability": ["durable", "lasting", "broke", "broken", "sturdy", "fragile"]
        }
        
        aspect_scores = {}
        
        for aspect, keywords in aspects.items():
            # Find sentences mentioning this aspect
            doc = nlp(text.lower())
            aspect_sentences = [sent.text for sent in doc.sents if any(kw in sent.text for kw in keywords)]
            
            if aspect_sentences:
                # Calculate average sentiment for this aspect
                sentiments = [self.vader.polarity_scores(sent)['compound'] for sent in aspect_sentences]
                avg_sentiment = sum(sentiments) / len(sentiments)
                
                # Scale to 0-100
                aspect_scores[aspect] = int((avg_sentiment + 1) * 50)
        
        return aspect_scores


# ============================================================================
# FEATURE 3: RECOMMENDATION SYSTEM
# ============================================================================

class RecommendationEngine:
    """Product recommendation without LLMs"""
    
    def __init__(self):
        self.products_df = None
        self.transactions_df = None
    
    def fit_collaborative_filtering(self, user_item_matrix: pd.DataFrame):
        """
        Train collaborative filtering model using SVD (Singular Value Decomposition)
        
        Args:
            user_item_matrix: DataFrame with users as rows, products as columns
                             Values are ratings or purchase count
        """
        # Convert to Surprise dataset format
        reader = Reader(rating_scale=(0, 5))
        data = Dataset.load_from_df(
            user_item_matrix.reset_index().melt(id_vars='index'),
            reader
        )
        
        # Train SVD model
        trainset = data.build_full_trainset()
        self.svd_model = SVD()
        self.svd_model.fit(trainset)
        
        print("✅ Collaborative filtering model trained")
    
    def recommend_collaborative(self, user_id: int, n_items: int = 5) -> List[str]:
        """Recommend products using collaborative filtering"""
        # Get predictions for all items
        predictions = []
        for item_id in range(100):  # Assuming 100 products
            pred = self.svd_model.predict(user_id, item_id)
            predictions.append((item_id, pred.est))
        
        # Sort by predicted rating
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        return [f"Product_{item_id}" for item_id, _ in predictions[:n_items]]
    
    def recommend_content_based(self, cart_items: List[str], all_products: List[Dict]) -> List[str]:
        """
        Content-based recommendations using TF-IDF and cosine similarity
        
        Args:
            cart_items: List of product names in cart
            all_products: List of product dicts with 'name', 'description', 'category'
        """
        # Create product descriptions corpus
        product_names = [p['name'] for p in all_products]
        descriptions = [f"{p['name']} {p.get('description', '')} {p.get('category', '')}" 
                       for p in all_products]
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        
        # Find cart items in product list
        cart_indices = [i for i, name in enumerate(product_names) if name in cart_items]
        
        if not cart_indices:
            return []
        
        # Calculate average vector for cart items
        cart_vector = tfidf_matrix[cart_indices].mean(axis=0)
        
        # Calculate similarity with all products
        similarities = cosine_similarity(cart_vector, tfidf_matrix).flatten()
        
        # Get top recommendations (excluding cart items)
        recommendations = []
        for idx in similarities.argsort()[::-1]:
            if idx not in cart_indices and len(recommendations) < 5:
                recommendations.append(product_names[idx])
        
        return recommendations
    
    def recommend_association_rules(self, transactions: pd.DataFrame, cart_items: List[str]) -> List[str]:
        """
        Use association rule mining (Apriori algorithm) for recommendations
        
        Args:
            transactions: DataFrame with transaction data (one-hot encoded products)
            cart_items: Current cart items
        """
        # Apply Apriori algorithm
        frequent_itemsets = apriori(transactions, min_support=0.01, use_colnames=True)
        
        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
        
        # Find rules where cart items are in antecedent
        recommendations = []
        for _, rule in rules.iterrows():
            antecedent = set(rule['antecedents'])
            consequent = set(rule['consequents'])
            
            # If cart items match antecedent, recommend consequent
            if antecedent.issubset(set(cart_items)):
                recommendations.extend(list(consequent))
        
        return list(set(recommendations))[:5]


# ============================================================================
# FEATURE 4: QUESTION ANSWERING (Retrieval-Based)
# ============================================================================

class ProductQA:
    """Answer product questions without LLMs using retrieval-based approach"""
    
    def __init__(self):
        self.qa_database = {}  # Product -> {question_pattern: answer_template}
        self.vectorizer = TfidfVectorizer()
    
    def add_qa_templates(self, product_name: str, qa_pairs: Dict[str, str]):
        """
        Add Q&A templates for a product
        
        Example:
            qa.add_qa_templates("Basmati Rice", {
                "how to cook": "To cook {product}, use 1:2 rice-to-water ratio. Boil and simmer for 15 mins.",
                "is it gluten free": "Yes, {product} is naturally gluten-free.",
                "shelf life": "{product} can be stored for up to 2 years in a cool, dry place."
            })
        """
        self.qa_database[product_name] = qa_pairs
    
    def answer_question(self, product_name: str, question: str) -> str:
        """
        Answer a question using pattern matching and template filling
        """
        if product_name not in self.qa_database:
            return "I don't have information about this product."
        
        templates = self.qa_database[product_name]
        
        # Find best matching template
        best_match = None
        best_score = 0
        
        for pattern, answer_template in templates.items():
            score = fuzz.partial_ratio(question.lower(), pattern.lower())
            if score > best_score:
                best_score = score
                best_match = answer_template
        
        if best_score > 60:  # Threshold
            # Fill template
            return best_match.replace("{product}", product_name)
        else:
            return "I'm not sure about that. Could you ask about cooking instructions, storage, or nutritional information?"


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_ai_search():
    """Example: AI Search without LLMs"""
    print("\n" + "="*80)
    print("EXAMPLE 1: AI SEARCH (Intent Detection + Entity Extraction)")
    print("="*80)
    
    # Training data
    training_data = [
        ("I want to make sushi", "recipe"),
        ("show me chicken recipes", "recipe"),
        ("buy fresh vegetables", "product"),
        ("need running shoes", "product"),
        ("best moisturizer for dry skin", "skincare"),
        ("face cream for oily skin", "skincare"),
        ("laptop under 1000 dollars", "electronics"),
    ]
    
    # Initialize and train
    search_engine = TraditionalAISearch()
    search_engine.train(training_data)
    
    # Available products
    products = [
        "Sushi Rice", "Nori Seaweed Sheets", "Rice Vinegar", 
        "Fresh Chicken Breast", "Basmati Rice", "Soy Sauce"
    ]
    
    # Test queries
    queries = [
        "I want to make sushi at home",
        "buy chicken for dinner",
    ]
    
    for query in queries:
        result = search_engine.search(query, products)
        print(f"\n📝 Query: '{query}'")
        print(f"   Type: {result['type']}")
        print(f"   Keywords: {result['keywords']}")
        print(f"   Matched Products: {result['ingredients']}")
        print(f"   Confidence: {result['confidence']:.2%}")


def example_sentiment_analysis():
    """Example: Sentiment Analysis without LLMs"""
    print("\n" + "="*80)
    print("EXAMPLE 2: SENTIMENT ANALYSIS")
    print("="*80)
    
    analyzer = SentimentAnalyzer()
    
    reviews = [
        "Great product! High quality but a bit expensive.",
        "Terrible quality, broke after one day. Do not buy!",
        "Good value for money. Fast delivery and excellent service.",
    ]
    
    for review in reviews:
        result = analyzer.analyze_review(review)
        print(f"\n📝 Review: '{review}'")
        print(f"   Positive: {result['positive']}%")
        print(f"   Negative: {result['negative']}%")
        print(f"   Aspects: {result['aspects']}")


def example_recommendations():
    """Example: Content-Based Recommendations"""
    print("\n" + "="*80)
    print("EXAMPLE 3: CONTENT-BASED RECOMMENDATIONS")
    print("="*80)
    
    recommender = RecommendationEngine()
    
    # Sample product database
    products = [
        {"name": "Chicken Breast", "description": "Fresh chicken protein", "category": "Meat"},
        {"name": "Soy Sauce", "description": "Asian sauce condiment", "category": "Pantry"},
        {"name": "Olive Oil", "description": "Cooking oil", "category": "Pantry"},
        {"name": "Fresh Vegetables", "description": "Mixed vegetables", "category": "Produce"},
        {"name": "Basmati Rice", "description": "Premium rice grain", "category": "Grains"},
        {"name": "Garam Masala", "description": "Indian spice blend", "category": "Spices"},
    ]
    
    cart = ["Chicken Breast", "Fresh Vegetables"]
    
    recommendations = recommender.recommend_content_based(cart, products)
    
    print(f"\n🛒 Cart Items: {cart}")
    print(f"✨ Recommended: {recommendations}")


def example_qa():
    """Example: Retrieval-Based Q&A"""
    print("\n" + "="*80)
    print("EXAMPLE 4: PRODUCT Q&A (Retrieval-Based)")
    print("="*80)
    
    qa_system = ProductQA()
    
    # Add Q&A templates
    qa_system.add_qa_templates("Basmati Rice", {
        "how to cook": "To cook Basmati Rice, rinse thoroughly, use 1:2 ratio (1 cup rice to 2 cups water), bring to boil, then simmer covered for 15 minutes. Let it rest for 5 minutes before serving.",
        "gluten free": "Yes, Basmati Rice is naturally gluten-free.",
        "storage": "Store Basmati Rice in an airtight container in a cool, dry place for up to 2 years.",
        "calories": "Basmati Rice contains approximately 200 calories per cooked cup.",
    })
    
    questions = [
        "How do I cook this rice?",
        "Is this gluten-free?",
        "What are the calories?",
    ]
    
    for question in questions:
        answer = qa_system.answer_question("Basmati Rice", question)
        print(f"\n❓ Q: {question}")
        print(f"💡 A: {answer}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n🤖 TRADITIONAL NLP IMPLEMENTATION (Without LLMs)")
    print("="*80)
    print("This demonstrates how to build AI features using classical NLP algorithms")
    print("instead of Large Language Models like GPT or Gemini.")
    print("="*80)
    
    example_ai_search()
    example_sentiment_analysis()
    example_recommendations()
    example_qa()
    
    print("\n" + "="*80)
    print("✅ All examples completed!")
    print("="*80)
