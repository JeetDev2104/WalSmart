# UPDATE Operations - Quick Reference Guide

## 📚 Table of Contents
1. [Single Product Update](#single-product-update)
2. [Bulk Updates](#bulk-updates)
3. [Conditional Updates](#conditional-updates)
4. [JSON Field Updates](#json-field-updates)
5. [Raw SQL Updates](#raw-sql-updates)
6. [Advanced Patterns](#advanced-patterns)

---

## 1. Single Product Update

### SQLAlchemy ORM
```python
from database import SessionLocal
from models import Product

db = SessionLocal()

# Find and update
product = db.query(Product).filter(Product.id == "prod-1").first()
if product:
    product.price = 15.99
    product.name = "Updated Name"
    db.commit()

db.close()
```

### Traditional SQL
```sql
UPDATE products 
SET price = 15.99, name = 'Updated Name'
WHERE id = 'prod-1';
```

---

## 2. Bulk Updates

### Update Multiple Products at Once

**ORM:**
```python
# Update all products in a category
db.query(Product).filter(
    Product.category == "Groceries"
).update({
    Product.price: Product.price * 1.1  # 10% increase
}, synchronize_session=False)

db.commit()
```

**SQL:**
```sql
UPDATE products 
SET price = price * 1.1 
WHERE category = 'Groceries';
```

---

## 3. Conditional Updates

### Update with Multiple Conditions

**ORM:**
```python
# Update products matching multiple criteria
db.query(Product).filter(
    Product.price < 10,
    Product.category == "Pantry"
).update({
    Product.price: 10.0,
    Product.description: Product.description + " - Minimum price"
}, synchronize_session=False)

db.commit()
```

**SQL:**
```sql
UPDATE products 
SET price = 10.0,
    description = description || ' - Minimum price'
WHERE price < 10 AND category = 'Pantry';
```

---

## 4. JSON Field Updates

### Update JSON/JSONB Columns

**ORM:**
```python
product = db.query(Product).filter(Product.id == "prod-1").first()

# Update entire JSON object
product.sentiment = {
    "positive": 90,
    "negative": 10,
    "aspects": {"quality": 95, "value": 85}
}

# Update array
product.tags = ["organic", "premium", "bestseller"]

db.commit()
```

**SQL:**
```sql
UPDATE products 
SET sentiment = '{"positive": 90, "negative": 10}',
    tags = '["organic", "premium", "bestseller"]'
WHERE id = 'prod-1';
```

---

## 5. Raw SQL Updates

### Using Raw SQL for Complex Operations

**ORM with Raw SQL:**
```python
from sqlalchemy import text

sql = text("""
    UPDATE products 
    SET price = ROUND(price * 1.05, 2),
        description = description || ' - Special Offer'
    WHERE category = :category 
    AND price > :min_price
""")

db.execute(sql, {"category": "Electronics", "min_price": 50})
db.commit()
```

**Traditional SQL:**
```sql
UPDATE products 
SET price = ROUND(price * 1.05, 2),
    description = description || ' - Special Offer'
WHERE category = 'Electronics' 
AND price > 50;
```

---

## 6. Advanced Patterns

### A. CASE Statement (Conditional Logic)

**ORM:**
```python
from sqlalchemy import case

db.query(Product).update({
    Product.price: case(
        (Product.price < 10, Product.price * 0.95),   # 5% off
        (Product.price < 50, Product.price * 0.90),   # 10% off
        else_=Product.price * 0.85                     # 15% off
    )
}, synchronize_session=False)

db.commit()
```

**SQL:**
```sql
UPDATE products 
SET price = CASE 
    WHEN price < 10 THEN price * 0.95
    WHEN price < 50 THEN price * 0.90
    ELSE price * 0.85
END;
```

### B. Batch Update from Dictionary

**ORM:**
```python
updates = {
    "prod-1": {"price": 14.99, "name": "New Name"},
    "prod-2": {"price": 8.99, "description": "New Description"}
}

for product_id, changes in updates.items():
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        for key, value in changes.items():
            setattr(product, key, value)

db.commit()
```

### C. Update with Validation

**ORM:**
```python
try:
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise ValueError("Product not found")
    
    if new_price <= 0:
        raise ValueError("Price must be positive")
    
    product.price = new_price
    db.commit()
    
except ValueError as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
```

### D. Update and Return Results

**ORM:**
```python
products = db.query(Product).filter(
    Product.category == "Skincare"
).all()

updated_products = []
for product in products:
    old_price = product.price
    product.price = product.price * 1.15
    updated_products.append({
        "name": product.name,
        "old_price": old_price,
        "new_price": product.price
    })

db.commit()
return updated_products
```

---

## 🎯 Common UPDATE Patterns

| **Use Case** | **ORM Pattern** | **SQL Pattern** |
|-------------|----------------|----------------|
| **Single field** | `product.price = 20; db.commit()` | `UPDATE products SET price=20 WHERE id='x'` |
| **Multiple fields** | `product.price=20; product.name='X'; db.commit()` | `UPDATE products SET price=20, name='X' WHERE id='x'` |
| **Bulk update** | `db.query(Product).filter(...).update({...})` | `UPDATE products SET ... WHERE ...` |
| **Price increase** | `Product.price: Product.price * 1.1` | `SET price = price * 1.1` |
| **String append** | `Product.desc: Product.desc + " text"` | `SET desc = desc || ' text'` |
| **Conditional** | `case((condition, value), else_=default)` | `CASE WHEN ... THEN ... ELSE ... END` |

---

## ⚠️ Important Notes

1. **synchronize_session**: Set to `False` for bulk updates to avoid session sync overhead
2. **Commit**: Always call `db.commit()` to save changes
3. **Rollback**: Use `db.rollback()` if an error occurs
4. **Close**: Always close the session with `db.close()`
5. **Validation**: Validate data before updating to prevent errors

---

## 🔧 Testing Updates

```python
# Check before update
product = db.query(Product).filter(Product.id == "prod-1").first()
print(f"Before: {product.price}")

# Perform update
product.price = 25.99
db.commit()

# Verify after update
db.refresh(product)
print(f"After: {product.price}")
```

---

## 📊 Update Statistics

```python
# Count affected rows
updated_count = db.query(Product).filter(
    Product.category == "Groceries"
).update({Product.price: Product.price * 1.1})

print(f"Updated {updated_count} products")
db.commit()
```

---

## 🚀 Running the Examples

```bash
# Run all UPDATE examples
cd ai-service
python3 update_examples.py

# Reset database if needed
python3 init_db.py
```

---

## 📝 Summary

- **ORM Approach**: More Pythonic, type-safe, database-agnostic
- **Raw SQL**: More control, better for complex queries
- **Best Practice**: Use ORM for most operations, raw SQL for complex logic
- **Always**: Validate → Update → Commit → Close

