from django.test import Client
from django.contrib.auth.models import User
import json
import sys

# Create a test client
client = Client()

# Authenticate with a user (adjust username as needed)
try:
    user = User.objects.first()
    if not user:
        print("No users found in the database.")
        sys.exit(1)
    
    client.force_login(user)
    
    # Get all categories
    from waste_logs.models import WasteCategory
    categories = WasteCategory.objects.all()
    
    if not categories:
        print("No categories found in the database.")
        sys.exit(1)
    
    # Test the get_subcategories endpoint for each category
    for category in categories:
        print(f"\nTesting category: {category.name}")
        response = client.get(f'/waste/get-subcategories/?category_id={category.id}')
        
        if response.status_code == 200:
            data = json.loads(response.content)
            subcategories = data.get('subcategories', [])
            
            print(f"Found {len(subcategories)} subcategories:")
            for sub in subcategories:
                print(f"- {sub['name']}")
        else:
            print(f"Error: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")
