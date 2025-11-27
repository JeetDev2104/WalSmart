import json

products = []

# Helper to add product
def add_product(id, name, description, price, image, category, sentiment, hint, tags=[]):
    products.append({
        "id": str(id),
        "name": name,
        "description": description,
        "longDescription": f"This is a premium {name}. {description} It is designed for high quality and customer satisfaction.",
        "price": price,
        "image": image,
        "category": category,
        "sentiment": sentiment,
        "dataAiHint": hint,
        "tags": tags
    })

# Start ID from 31
current_id = 31

# Rice
rice_varieties = [
    ("Sona Masoori Rice", "Lightweight and aromatic medium-grain rice.", 15.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Brown Basmati Rice", "Whole grain goodness with a nutty flavor.", 14.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Jasmine Rice 10lb", "Fragrant long-grain rice for family meals.", 18.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Arborio Rice", "Creamy and starchy, perfect for risotto.", 8.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Sushi Rice", "Sticky and short-grain, ideal for sushi rolls.", 9.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Wild Rice Mix", "Nutty and chewy blend of wild and long-grain rice.", 11.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Red Cargo Rice", "Nutrient-rich unpolished rice with a chewy texture.", 10.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Black Rice", "Antioxidant-rich 'forbidden rice' with a sweet flavor.", 12.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Parboiled Rice", "Partially boiled in the husk, retains more vitamins.", 7.99, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
    ("Sticky Glutinous Rice", "Sweet and sticky, great for desserts and dumplings.", 8.49, "https://images.unsplash.com/photo-1586201375761-83865001e30c?auto=format&fit=crop&w=800&q=60"),
]

for name, desc, price, img in rice_varieties:
    add_product(current_id, name, desc, price, img, "Pantry", 
                {"positive": 90, "negative": 10, "aspects": {"quality": 92, "taste": 90, "freshness": 95}}, 
                "rice", ["ingredient: rice dish", "pantry staple"])
    current_id += 1

# Sauces & Spices
spices = [
    ("Dark Soy Sauce", "Rich and thick soy sauce for coloring and flavor.", 4.99, "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=crop&w=800&q=60", "soy sauce"),
    ("Light Soy Sauce", "Salty and thin, essential for seasoning.", 3.99, "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=crop&w=800&q=60", "soy sauce"),
    ("Oyster Sauce", "Savory and sweet sauce for stir-fries.", 5.49, "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=crop&w=800&q=60", "oyster sauce"),
    ("Sesame Oil", "Toasted sesame oil for aromatic finishing.", 6.99, "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=60", "oil"),
    ("Chili Oil", "Spicy oil infused with chili flakes.", 5.99, "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=60", "oil"),
    ("Turmeric Powder", "Bright yellow spice with earthy flavor.", 3.49, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=60", "spice"),
    ("Cumin Seeds", "Warm and earthy seeds for tempering.", 2.99, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=60", "spice"),
    ("Coriander Powder", "Citrusy and nutty ground coriander.", 3.29, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=60", "spice"),
    ("Garam Masala", "Aromatic blend of warming spices.", 4.49, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=60", "spice"),
    ("Red Chili Powder", "Spicy ground chilies for heat.", 3.99, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=60", "spice"),
]

for name, desc, price, img, hint in spices:
    add_product(current_id, name, desc, price, img, "Pantry", 
                {"positive": 94, "negative": 6, "aspects": {"flavor": 96, "quality": 93}}, 
                hint, ["ingredient: cooking", "pantry staple"])
    current_id += 1

# Jackets
jackets = [
    ("Arctic Parka", "Heavy-duty winter parka with faux fur hood.", 199.99, "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Bomber Jacket", "Classic style bomber jacket in olive green.", 89.99, "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Leather Biker Jacket", "Genuine leather jacket with asymmetrical zip.", 249.99, "https://images.unsplash.com/photo-1551028919-30164bdc5800?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Windbreaker", "Lightweight and colorful windbreaker for sports.", 49.99, "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Trench Coat", "Elegant beige trench coat for rainy days.", 129.99, "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Quilted Vest", "Warm sleeveless vest for layering.", 59.99, "https://images.unsplash.com/photo-1613715642502-735a725f522c?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Ski Jacket", "Waterproof and insulated jacket for snow sports.", 179.99, "https://images.unsplash.com/photo-1608256249259-8367ca9b2c89?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Varsity Jacket", "Collegiate style jacket with wool body.", 99.99, "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Faux Fur Coat", "Luxurious and soft faux fur coat.", 149.99, "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&w=800&q=60", "Jackets"),
    ("Rain Poncho", "Packable waterproof poncho.", 29.99, "https://images.unsplash.com/photo-1628427255527-e1c4e1a1a6d2?auto=format&fit=crop&w=800&q=60", "Jackets"),
]

for name, desc, price, img, cat in jackets:
    add_product(current_id, name, desc, price, img, cat, 
                {"positive": 92, "negative": 8, "aspects": {"warmth": 95, "style": 94, "comfort": 90}}, 
                "jacket", ["clothing", "outerwear"])
    current_id += 1

# Electronics
electronics = [
    ("Noise Cancelling Headphones", "Over-ear headphones with active noise cancellation.", 299.99, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Wireless Earbuds", "True wireless earbuds with charging case.", 129.99, "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Smartwatch Series 5", "Fitness tracker and smartwatch with heart rate monitor.", 199.99, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("4K Action Camera", "Waterproof action camera for capturing adventures.", 149.99, "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Bluetooth Speaker", "Portable speaker with 360-degree sound.", 79.99, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Gaming Mouse", "Ergonomic mouse with customizable RGB lighting.", 59.99, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Mechanical Keyboard", "Tactile mechanical keyboard for typing and gaming.", 89.99, "https://images.unsplash.com/photo-1587829741301-dc798b91a603?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Tablet Pro 11", "High-performance tablet for creativity and work.", 699.99, "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("E-Reader", "Glare-free display for comfortable reading.", 119.99, "https://images.unsplash.com/photo-1592434134753-a70baf7979d5?auto=format&fit=crop&w=800&q=60", "Electronics"),
    ("Smart Home Hub", "Voice-controlled hub for smart home devices.", 99.99, "https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&w=800&q=60", "Electronics"),
]

for name, desc, price, img, cat in electronics:
    add_product(current_id, name, desc, price, img, cat, 
                {"positive": 95, "negative": 5, "aspects": {"performance": 96, "quality": 94, "value": 90}}, 
                "electronics", ["gadget", "tech"])
    current_id += 1


# Read existing products.ts
ts_file_path = "project/src/data/products.ts"
with open(ts_file_path, "r") as f:
    ts_content = f.read()

# Find the last occurrence of "];"
last_bracket_index = ts_content.rfind("];")

if last_bracket_index != -1:
    # Prepare new products string (JSON format is valid TS)
    # We strip the outer [ and ] from the JSON dump
    new_products_str = json.dumps(products, indent=2)[1:-1]
    
    # Construct new content
    # Add a comma before the new products if the list wasn't empty (it wasn't)
    new_content = ts_content[:last_bracket_index] + "," + new_products_str + "];"
    
    with open(ts_file_path, "w") as f:
        f.write(new_content)
    print("Successfully appended products to products.ts")
else:
    print("Could not find closing bracket in products.ts")

