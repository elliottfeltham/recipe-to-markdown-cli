import requests
import html
import json
from bs4 import BeautifulSoup

# URLs for testing purposes
test_url_1 = "https://www.bbcgoodfood.com/recipes/pasta-alla-vodka"
test_url_2 = "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake"
test_url_3 = "https://www.allrecipes.com/recipe/30522/unbelievable-chicken/"

# Send requests to recipe website
response = requests.get(test_url_2, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
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
    
    # Find the correct recipe script
    if data.get("@type") == "Recipe":
        title = data.get("name").title()
        servings = data.get("recipeYield")
        ingredients = data.get("recipeIngredient")
        steps = []

        for step in data.get("recipeInstructions"):
            
            steps.append(step.get("text"))

        # Format recipe
        print(f"{title}\n")

        print(f"Serves: {servings}\n")

        print("Ingredients:")
        print("\n".join(ingredients))
        print("\n")

        print("Method:")
        for index, step in enumerate(steps, start=1):
            print(f"{index}: {step}")

        break
        
    

