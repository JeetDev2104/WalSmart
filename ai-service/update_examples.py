"""
UPDATE Operations Examples for WalSmart Product Database
Demonstrates various ways to update product information using SQLAlchemy ORM
"""

from sqlalchemy import func
from database import SessionLocal
from models import Product
import json

def update_single_product_by_id():
    """Update a single product by its ID"""
    print("\n=== UPDATE SINGLE PRODUCT BY ID ===")
    db = SessionLocal()
    
    # Find product by ID
    product = db.query(Product).filter(Product.id == "prod-1").first()
    
    if product:
        print(f"Before: {product.name} - ${product.price}")
        
        # Update fields
        product.price = 15.99
        product.name = "Premium Basmati Rice - Updated"
        product.description = "Updated description with new features"
        
        # Commit changes
        db.commit()
        
        print(f"After: {product.name} - ${product.price}")
        print("✓ Product updated successfully!")
    else:
        print("✗ Product not found")
    
    db.close()


def update_product_price_increase():
    """Increase prices for all products in a category"""
    print("\n=== BULK PRICE UPDATE (10% INCREASE) ===")
    db = SessionLocal()
    
    category = "Groceries"
    
    # Get products before update
    products_before = db.query(Product).filter(
        Product.category == category
    ).all()
    
    print(f"Products in {category} before update:")
    for p in products_before[:3]:  # Show first 3
        print(f"  {p.name}: ${p.price}")
    
    # Bulk update - increase price by 10%
    updated_count = db.query(Product).filter(
        Product.category == category
    ).update({
        Product.price: Product.price * 1.1
    }, synchronize_session=False)
    
    db.commit()
    
    # Get products after update
    products_after = db.query(Product).filter(
        Product.category == category
    ).all()
    
    print(f"\nProducts in {category} after 10% increase:")
    for p in products_after[:3]:  # Show first 3
        print(f"  {p.name}: ${p.price:.2f}")
    
    print(f"\n✓ Updated {updated_count} products")
    
    db.close()


def update_with_conditions():
    """Update products based on multiple conditions"""
    print("\n=== UPDATE WITH MULTIPLE CONDITIONS ===")
    db = SessionLocal()
    
    # Update all products that are cheap AND in Pantry category
    updated_count = db.query(Product).filter(
        Product.price < 10,
        Product.category == "Pantry"
    ).update({
        Product.price: 10.0,
        Product.description: Product.description + " - Price adjusted to minimum"
    }, synchronize_session=False)
    
    db.commit()
    
    print(f"✓ Set minimum price of $10 for {updated_count} cheap pantry items")
    
    db.close()


def update_json_field():
    """Update JSON fields (sentiment, tags)"""
    print("\n=== UPDATE JSON FIELDS ===")
    db = SessionLocal()
    
    product = db.query(Product).filter(Product.id == "prod-1").first()
    
    if product:
        print(f"Product: {product.name}")
        print(f"Before sentiment: {product.sentiment}")
        
        # Update sentiment JSON
        new_sentiment = {
            "positive": 90,
            "negative": 10,
            "aspects": {
                "quality": 95,
                "value": 85,
                "taste": 92
            }
        }
        product.sentiment = new_sentiment
        
        # Update tags JSON
        product.tags = ["organic", "premium", "bestseller", "gluten-free"]
        
        db.commit()
        
        print(f"After sentiment: {product.sentiment}")
        print(f"After tags: {product.tags}")
        print("✓ JSON fields updated successfully!")
    
    db.close()


def update_using_raw_sql():
    """Update using raw SQL for complex operations"""
    print("\n=== UPDATE USING RAW SQL ===")
    from sqlalchemy import text
    db = SessionLocal()
    
    # Raw SQL update
    sql = text("""
        UPDATE products 
        SET price = ROUND(price * 1.05, 2),
            description = description || ' - Special Offer'
        WHERE category = :category 
        AND price > :min_price
    """)
    
    result = db.execute(sql, {
        "category": "Electronics",
        "min_price": 50
    })
    
    db.commit()
    
    print(f"✓ Updated {result.rowcount} electronics with 5% price increase")
    
    db.close()


def update_with_case_statement():
    """Conditional update using CASE statement"""
    print("\n=== CONDITIONAL UPDATE (CASE STATEMENT) ===")
    from sqlalchemy import case
    db = SessionLocal()
    
    # Apply different discounts based on price range
    db.query(Product).update({
        Product.price: case(
            (Product.price < 10, Product.price * 0.95),   # 5% off for cheap items
            (Product.price < 50, Product.price * 0.90),   # 10% off for mid-range
            else_=Product.price * 0.85                     # 15% off for expensive items
        )
    }, synchronize_session=False)
    
    db.commit()
    
    print("✓ Applied tiered discounts based on price ranges")
    print("  - Under $10: 5% off")
    print("  - $10-$50: 10% off")
    print("  - Over $50: 15% off")
    
    db.close()


def update_and_return_updated():
    """Update products and return the updated records"""
    print("\n=== UPDATE AND RETURN RESULTS ===")
    db = SessionLocal()
    
    # Get products to update
    products = db.query(Product).filter(
        Product.category == "Skincare",
        Product.price < 30
    ).all()
    
    print(f"Updating {len(products)} skincare products...")
    
    updated_products = []
    for product in products:
        old_price = product.price
        product.price = product.price * 1.15  # 15% increase
        updated_products.append({
            "name": product.name,
            "old_price": old_price,
            "new_price": product.price
        })
    
    db.commit()
    
    print("\nUpdated products:")
    for item in updated_products:
        print(f"  {item['name']}: ${item['old_price']:.2f} → ${item['new_price']:.2f}")
    
    db.close()


def update_with_validation():
    """Update with validation and error handling"""
    print("\n=== UPDATE WITH VALIDATION ===")
    db = SessionLocal()
    
    try:
        product_id = "prod-1"
        new_price = 25.99
        
        # Validate product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        # Validate price is positive
        if new_price <= 0:
            raise ValueError("Price must be positive")
        
        # Validate price is not too high
        if new_price > 1000:
            raise ValueError("Price exceeds maximum allowed value")
        
        # Update
        old_price = product.price
        product.price = new_price
        db.commit()
        
        print(f"✓ {product.name}: ${old_price:.2f} → ${new_price:.2f}")
        
    except ValueError as e:
        db.rollback()
        print(f"✗ Validation error: {e}")
    except Exception as e:
        db.rollback()
        print(f"✗ Update failed: {e}")
    finally:
        db.close()


def batch_update_from_dict():
    """Update multiple products from a dictionary"""
    print("\n=== BATCH UPDATE FROM DICTIONARY ===")
    db = SessionLocal()
    
    # Dictionary of product updates
    updates = {
        "prod-1": {"price": 14.99, "name": "Basmati Rice - Family Pack"},
        "prod-2": {"price": 8.99, "description": "Fresh organic vegetables"},
        "prod-3": {"price": 22.50, "category": "Premium Groceries"}
    }
    
    updated_count = 0
    for product_id, changes in updates.items():
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in changes.items():
                setattr(product, key, value)
            updated_count += 1
            print(f"✓ Updated {product.name}")
    
    db.commit()
    print(f"\nTotal updated: {updated_count} products")
    
    db.close()


def update_statistics():
    """Show update statistics and affected rows"""
    print("\n=== UPDATE STATISTICS ===")
    db = SessionLocal()
    
    # Count products before update
    total_before = db.query(Product).count()
    category_count_before = db.query(Product).filter(
        Product.category == "Groceries"
    ).count()
    
    print(f"Total products: {total_before}")
    print(f"Groceries before: {category_count_before}")
    
    # Perform update
    updated = db.query(Product).filter(
        Product.category == "Groceries",
        Product.price < 15
    ).update({
        Product.dataAiHint: Product.dataAiHint + " affordable grocery"
    }, synchronize_session=False)
    
    db.commit()
    
    print(f"\n✓ Updated {updated} affordable grocery items")
    print(f"  ({(updated/category_count_before)*100:.1f}% of groceries)")
    
    db.close()


# Traditional SQL equivalents for reference
SQL_EXAMPLES = """
=== TRADITIONAL SQL EQUIVALENTS ===

1. Update single product:
   UPDATE products 
   SET price = 15.99, name = 'Premium Basmati Rice - Updated'
   WHERE id = 'prod-1';

2. Bulk price increase:
   UPDATE products 
   SET price = price * 1.1 
   WHERE category = 'Groceries';

3. Update with conditions:
   UPDATE products 
   SET price = 10.0,
       description = description || ' - Price adjusted to minimum'
   WHERE price < 10 AND category = 'Pantry';

4. Update JSON field (SQLite):
   UPDATE products 
   SET sentiment = '{"positive": 90, "negative": 10}'
   WHERE id = 'prod-1';

5. Conditional update (CASE):
   UPDATE products 
   SET price = CASE 
       WHEN price < 10 THEN price * 0.95
       WHEN price < 50 THEN price * 0.90
       ELSE price * 0.85
   END;

6. Update with subquery:
   UPDATE products 
   SET price = (SELECT AVG(price) FROM products WHERE category = 'Groceries')
   WHERE category = 'Groceries' AND price < 5;
"""


if __name__ == "__main__":
    print("=" * 60)
    print("🛒 WalSmart Product Database - UPDATE Examples")
    print("=" * 60)
    
    # Run all examples
    update_single_product_by_id()
    update_product_price_increase()
    update_with_conditions()
    update_json_field()
    update_using_raw_sql()
    update_with_case_statement()
    update_and_return_updated()
    update_with_validation()
    batch_update_from_dict()
    update_statistics()
    
    # Show SQL equivalents
    print("\n" + "=" * 60)
    print(SQL_EXAMPLES)
    print("=" * 60)
    
    print("\n✅ All UPDATE examples completed!")
    print("\n⚠️  Note: Some updates modify actual data.")
    print("   Run init_db.py to reset the database if needed.")
