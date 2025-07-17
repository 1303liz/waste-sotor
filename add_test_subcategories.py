from waste_logs.models import WasteCategory, WasteSubcategory
from django.db import transaction

def add_test_subcategories():
    """Add test subcategories to each waste category"""
    with transaction.atomic():
        # First, clear existing subcategories to avoid duplicates
        WasteSubcategory.objects.all().delete()
        
        # Get all categories
        categories = WasteCategory.objects.all()
        
        for category in categories:
            # Add test subcategories
            WasteSubcategory.objects.create(
                category=category,
                name=f"{category.name} - Type A",
                description=f"Test subcategory A for {category.name}",
                recycling_instructions="Test instructions"
            )
            
            WasteSubcategory.objects.create(
                category=category,
                name=f"{category.name} - Type B",
                description=f"Test subcategory B for {category.name}",
                recycling_instructions="Test instructions"
            )
            
            WasteSubcategory.objects.create(
                category=category,
                name=f"{category.name} - Type C",
                description=f"Test subcategory C for {category.name}",
                recycling_instructions="Test instructions"
            )
        
        print(f"Added {WasteSubcategory.objects.count()} test subcategories")

# Run the function
add_test_subcategories()
