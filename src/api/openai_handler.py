"""
Module for handling API requests to OpenAI services.
"""
import base64
import requests
from typing import Dict, Any, List, Optional
from io import BytesIO
from PIL import Image

# Try to import openai, but make it optional
try:
    import openai
except ImportError:
    openai = None


def encode_image(image_bytes: bytes) -> str:
    """
    Encode an image to base64 for API transmission.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        str: Base64 encoded image string
    """
    base64_image = base64.b64encode(image_bytes).decode()
    return base64_image


def get_openai_headers(api_key: str) -> Dict[str, str]:
    """
    Generate headers for OpenAI API requests.
    
    Args:
        api_key (str): OpenAI API key
        
    Returns:
        Dict[str, str]: Headers dictionary for API requests
    """
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


def extract_ingredients_from_image(image_bytes: bytes, api_key: str, endpoint: str, model: str, max_tokens: int) -> str:
    """
    Use OpenAI's Vision model to extract ingredients from an image.
    
    Args:
        image_bytes (bytes): Raw image bytes
        api_key (str): OpenAI API key
        endpoint (str): API endpoint URL
        model (str): Model name to use
        max_tokens (int): Maximum tokens for response
        
    Returns:
        str: Extracted ingredients text
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    # Encode the image
    base64_image = encode_image(image_bytes)
    
    # Headers for the request
    headers = get_openai_headers(api_key)
    
    # Payload for the request
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Focus on identifying food ingredients in the image. First, locate any section labeled 'Ingredients:' or 'INGREDIENTS'. Then extract ONLY the actual ingredient names themselves (like water, sugar, flour, etc.) that follow this heading. Ignore any non-ingredient text. Return the ingredients as a simple comma-separated list. If there's no explicit ingredients label, identify the list of food additives and ingredients directly from the packaging based on their appearance and position. Focus on detecting actual food ingredients regardless of their position or formatting on the package."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }
    
    # Make the API request to OpenAI
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()  # Raise exception for HTTP errors
    
    # Extract content from response
    response_data = response.json()
    ingredients_text = response_data['choices'][0]['message']['content']
    
    return ingredients_text


def query_openai_about_ingredients(ingredient_list: List[str], api_key: str, endpoint: str) -> str:
    """
    Query OpenAI about the halal status of unknown ingredients.
    
    Args:
        ingredient_list (List[str]): List of ingredients to query
        api_key (str): OpenAI API key
        endpoint (str): API endpoint URL
        
    Returns:
        str: OpenAI's response about the ingredients
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    headers = get_openai_headers(api_key)
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides information."},
            {"role": "user", "content": f"Determine if the ingredients in '{ingredient_list}' are halal."}
        ]
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']