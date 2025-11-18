"""
Module for parsing and processing ingredient text extracted from images.
"""
import re
from typing import List, Tuple, Dict, Optional

def parse_ingredients(ingredients_text: str) -> List[str]:
    """
    Parse a string of ingredients text into a list of individual ingredients.
    
    Args:
        ingredients_text (str): Raw text containing ingredients list
        
    Returns:
        List[str]: List of parsed individual ingredients
    """
    # Normalize the text
    ingredients_text = ingredients_text.lower().replace("[", "(").replace("]", ")")
    
    # Remove newline characters
    ingredients_text = ingredients_text.replace("\n", ",")

    # Remove the portion starting from "allergen information:"
    ingredients_text = re.sub(r'allergen information:.*|allergen information.*', '', ingredients_text)
    
    # Regular expression to remove everything after "Contains" up to a period or the end of the string
    ingredients_text = re.sub(r'(contains|may contain:).*?(\.|$)', '', ingredients_text)

    # Replace specific phrases
    phrases_to_remove = [
        "the ingredients listed in the image are:\n\n", 
        "ingredients:", 
        'the ingredients listed on the image', 
        "here are the ingredients as listed on the image:\n\n ", 
        "here are the ingredients as listed on the image: ", 
        "are as follows:  -",
        "the ingredients listed on the image are as follows:\n\n ", 
        "are as follows:", 
        "are:", 
        "the ingredients listed", 
        "the image shows a list of ingredients", 
        "which includes items like", 
        "the list is a typical example of ingredients you might find on the packaging of a processed food product",
        "and it provides important information for consumers about what is in the product as well as potential allergens they should be aware of",
        "the text also mentions",
        "here are the ingredients exactly as they appear in the image:", 
        "sure", 
        "here is the list of ingredients exactly as they appear in the image:", 
        "in the image", 
        "the ingredients  are listed as follows:", 
        "on the packaging",
        "the ingredients exactly as they appear"
    ]
    
    for phrase in phrases_to_remove:
        ingredients_text = ingredients_text.replace(phrase, "")

    # Replace remaining "\n" with ", "
    ingredients_text = ingredients_text.replace("\n", "")
        
    # Replace semicolons with commas
    ingredients_text = ingredients_text.replace(';', ',')
    
    # Remove a full stop at the end if it exists
    ingredients_text = ingredients_text.rstrip('.')
    
    # Replace remaining "-" with ", "
    ingredients_text = ingredients_text.replace("-", "")
    
    # Remove any periods ('.')
    ingredients_text = ingredients_text.replace('.', '')
    
    # Split based on commas not within parentheses
    ingredients = re.split(r',\s*(?![^()]*\))', ingredients_text)
    
    # Strip whitespace from each ingredient
    parsed_ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]
    return parsed_ingredients


def create_lookup_table(df) -> Dict[str, str]:
    """
    Create a lookup table from the pre-processed ingredients DataFrame.
    
    Args:
        df: Pandas DataFrame containing ingredient data
        
    Returns:
        Dict[str, str]: Dictionary mapping ingredient names to halal status
    """
    # Use only required columns and create a dictionary for lookup
    lookup_table = df.set_index('ingred_name')['halal_non_halal_doubtful'].to_dict()
    return lookup_table


def check_halal_status(ingredients: List[str], lookup_table: Dict[str, str]) -> Tuple[str, List[str]]:
    """
    Check the halal status of a list of ingredients against a lookup table.
    
    Args:
        ingredients (List[str]): List of ingredient names
        lookup_table (Dict[str, str]): Dictionary mapping ingredient names to halal status
        
    Returns:
        Tuple[str, List[str]]: Tuple containing (product_halal_status, list of unknown ingredients)
    """
    product_halal_status = 'Halal'  # Default status
    unknown_ingredients = []

    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()

        # Check the Halal status from the lookup table
        status = lookup_table.get(ingredient_lower, "Unknown")

        if status == 'Non-Halal' or status == 'Doubtful':  # Non-halal or doubtful
            product_halal_status = 'Non-Halal'
        elif status == "Unknown":
            product_halal_status = 'Doubtful'
            unknown_ingredients.append(ingredient)

    # Return a tuple: product status and list of unknown ingredients
    return product_halal_status, unknown_ingredients