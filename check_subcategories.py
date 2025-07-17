from waste_logs.models import WasteCategory, WasteSubcategory

# Check categories
print("Categories:")
categories = WasteCategory.objects.all()
for category in categories:
    print(f"- {category.name}")

# Check subcategories
print("\nSubcategories:")
for category in categories:
    subcategories = category.subcategories.all()
    if subcategories:
        print(f"\n{category.name} subcategories:")
        for subcategory in subcategories:
            print(f"- {subcategory.name}")
    else:
        print(f"\n{category.name}: No subcategories")
