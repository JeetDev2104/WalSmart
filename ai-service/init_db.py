import json
import re
from database import engine, SessionLocal
from models import Base, Product

def extract_products_from_ts(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the array content between "export const products: Product[] = [" and "];"
    match = re.search(r'export const products: Product\[\] = \[\s*(.*)\s*\];', content, re.DOTALL)
    if not match:
        print("Could not find products array")
        return []
    
    array_content = match.group(1)
    
    # Basic cleanup to make it valid JSON-ish for python parsing
    # This is a bit hacky but avoids needing a full TS parser
    # 1. Quote keys
    # 2. Convert single quotes to double quotes
    # 3. Handle trailing commas
    
    products = []
    # Split by object boundaries roughly
    items = array_content.split('},\n  {')
    
    for item in items:
        item = item.strip().strip('{').strip('}')
        product = {}
        
        # Extract fields using regex
        id_match = re.search(r"id:\s*['\"](.*?)['\"]", item)
        name_match = re.search(r"name:\s*['\"](.*?)['\"]", item)
        desc_match = re.search(r"description:\s*['\"](.*?)['\"]", item)
        long_desc_match = re.search(r"longDescription:\s*['\"](.*?)['\"]", item)
        price_match = re.search(r"price:\s*([\d.]+)", item)
        image_match = re.search(r"image:\s*['\"](.*?)['\"]", item)
        cat_match = re.search(r"category:\s*['\"](.*?)['\"]", item)
        hint_match = re.search(r"dataAiHint:\s*['\"](.*?)['\"]", item)
        
        # Tags
        tags_match = re.search(r"tags:\s*\[(.*?)\]", item)
        tags = []
        if tags_match:
            tags_str = tags_match.group(1)
            tags = [t.strip().strip("'").strip('"') for t in tags_str.split(',')]

        # Sentiment
        sentiment = {}
        sent_match = re.search(r"sentiment:\s*{(.*?)}", item, re.DOTALL)
        if sent_match:
            sent_content = sent_match.group(1)
            pos_match = re.search(r"positive:\s*(\d+)", sent_content)
            neg_match = re.search(r"negative:\s*(\d+)", sent_content)
            
            aspects = {}
            aspects_match = re.search(r"aspects:\s*{(.*?)}", sent_content, re.DOTALL)
            if aspects_match:
                aspects_content = aspects_match.group(1)
                for aspect in aspects_content.split(','):
                    parts = aspect.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip()
                        aspects[key] = int(val)
            
            sentiment = {
                "positive": int(pos_match.group(1)) if pos_match else 0,
                "negative": int(neg_match.group(1)) if neg_match else 0,
                "aspects": aspects
            }

        if id_match:
            product = {
                "id": id_match.group(1),
                "name": name_match.group(1) if name_match else "",
                "description": desc_match.group(1) if desc_match else "",
                "longDescription": long_desc_match.group(1) if long_desc_match else "",
                "price": float(price_match.group(1)) if price_match else 0.0,
                "image": image_match.group(1) if image_match else "",
                "category": cat_match.group(1) if cat_match else "",
                "dataAiHint": hint_match.group(1) if hint_match else "",
                "tags": tags,
                "sentiment": sentiment
            }
            products.append(product)
            
    return products

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if data exists
    if db.query(Product).count() > 0:
        print("Database already initialized.")
        db.close()
        return

    print("Extracting data from products.ts...")
    products_data = extract_products_from_ts("../project/src/data/products.ts")
    
    print(f"Found {len(products_data)} products.")
    
    for p_data in products_data:
        db_product = Product(**p_data)
        db.add(db_product)
    
    db.commit()
    print("Database populated successfully!")
    db.close()

if __name__ == "__main__":
    init_db()
