import requests
import html
import json
from bs4 import BeautifulSoup



# URLs for testing purposes
test_url = input("Enter recipe URL to extract JSON: ")


response = requests.get(test_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()

# Recipe webpage string
recipe_webpage = response.text

# Use the Beautiful Soup library to parse the HTML and find the recipe scripts
soup = BeautifulSoup(recipe_webpage, 'html.parser')
scripts = soup.find_all("script", {"type": "application/ld+json"})

for tag in scripts:
        # Turn the JSON text in a dict or a list with error handling
        try:
            data = json.loads(html.unescape(tag.get_text() or ""))
        except json.JSONDecodeError:
            continue

        
        # Successfully extracts from lists 
        if isinstance(data, list):
            for obj in data:
                json.dumps(obj, indent=2)
                if obj.get("@type") == "Recipe":
                    print({"title": obj.get("name").title(), 
                        "servings": obj.get("recipeYield"), 
                        "ingredients": obj.get("recipeIngredient"), 
                        "steps": obj.get("recipeInstructions")})
             


