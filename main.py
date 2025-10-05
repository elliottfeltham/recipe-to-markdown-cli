import requests
import html
import json
from bs4 import BeautifulSoup

RECIPES_FOLDER_PATH = "/Users/elliottfeltham/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidiannotes/Areas/Recipes/"

# URLs for testing purposes
test_url = "https://www.allrecipes.com/recipe/30522/unbelievable-chicken/"


def extract_recipe(url: str):
    # Send requests to recipe website
    response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
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
             return {"title": data.get("name").title(), 
                    "servings": data.get("recipeYield"), 
                    "ingredients": data.get("recipeIngredient"), 
                    "steps": data.get("recipeInstructions"),
                    "source": url}
            
    # Return None if nothing found
    return None

                
# Format recipe function
def format_recipe_to_markdown(recipe: dict):
    ingredients = []
    for ingredient in recipe["ingredients"]:
        ingredients.append(f"+ {ingredient} \n")

    steps = []
    for step in recipe["steps"]:
        steps.append(step.get("text"))

    method = []
    for index, step in enumerate(steps, start=1):
        method.append(f"{index}. {step}\n\n")

    with open(f"{RECIPES_FOLDER_PATH}/{recipe["title"]}.md", "w") as file:
        # For my own obsidian tagging system
        file.write("> [!tags]- tags\n")
        
        # Write recipe in markdown
        file.write(f"*Serves: {recipe["servings"]} people*\n\n"
                    "## Ingredients:\n\n")
        file.writelines(ingredients)
        file.write(f"\n\n" 
                    "## Method:\n\n")
        file.writelines(method)
        file.write(f"\n\n" 
                    f"[Visit the website]({recipe["source"]})")
        
def main():
    # Get the URL from the user and extract the webpage information
    recipe_url = input("Paste a recipe's URL to send it to your notes: ").strip()
    recipe = extract_recipe(recipe_url)

    # Print a message if recipe not extracted
    if not recipe:
        print("No Recipe JSON-LD found on that page.")
        return
    
    # Format recipe and write it to notes
    format_recipe_to_markdown(recipe)
    print("Successfully saved to your notes!")
                    
main()