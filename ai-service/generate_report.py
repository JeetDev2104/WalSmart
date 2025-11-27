from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def generate_report():
    db = SessionLocal()
    products = db.query(models.Product).all()
    
    report = "# Product Verification Report\n\n"
    report += "| ID | Name | Category | Price | Image |\n"
    report += "|---|---|---|---|---|\n"
    
    for p in products:
        report += f"| {p.id} | {p.name} | {p.category} | ${p.price} | [Link]({p.image}) |\n"
    
    with open("product_report.md", "w") as f:
        f.write(report)
    
    print("Report generated: product_report.md")
    db.close()

if __name__ == "__main__":
    generate_report()
