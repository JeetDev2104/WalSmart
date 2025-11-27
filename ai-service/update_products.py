from database import SessionLocal
from models import Product

def update_products():
    db = SessionLocal()
    
    # User corrected ID 6 -> ID 9
    updates = [
        {"id": "9", "image": "https://batteryworldonline.com/cdn/shop/products/uscb-c-super-fast-wall-charger6ft-cable-for-samsung-galaxy-s20-s21-s22-754492.jpg?v=1703095248"},
    ]

    print(f"Starting update for {len(updates)} products...")
    
    updated_count = 0
    not_found_count = 0
    
    for item in updates:
        product = db.query(Product).filter(Product.id == item["id"]).first()
        if product:
            product.image = item["image"]
            if "price" in item:
                product.price = item["price"]
            updated_count += 1
            print(f"Updated product {item['id']}")
        else:
            not_found_count += 1
            print(f"Product {item['id']} not found")
            
    db.commit()
    db.close()
    print(f"\nFinished. Updated: {updated_count}, Not Found: {not_found_count}")

if __name__ == "__main__":
    update_products()
