"""
Configuration settings for the Halal Ingredient Analysis application.
"""
import os
import toml
from pathlib import Path

# Define base paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
STORAGE_DIR = ROOT_DIR / "storage"
ASSETS_DIR = ROOT_DIR / "assets"

# Create assets directory if it doesn't exist
if not ASSETS_DIR.exists():
    ASSETS_DIR.mkdir()

# Move snack.jpg to assets directory if it's in the root and assets directory exists
SNACK_IMAGE_PATH = ROOT_DIR / "snack.jpg"
ASSET_IMAGE_PATH = ASSETS_DIR / "snack.jpg"
if SNACK_IMAGE_PATH.exists() and ASSETS_DIR.exists() and not ASSET_IMAGE_PATH.exists():
    import shutil
    shutil.copy(SNACK_IMAGE_PATH, ASSET_IMAGE_PATH)

# Image paths
BACKGROUND_IMAGE = str(ASSET_IMAGE_PATH if ASSET_IMAGE_PATH.exists() else SNACK_IMAGE_PATH)

# API Configuration
def load_api_config():
    """
    Load API configuration from multiple sources with priority:
    1. secrets.toml file in the root directory
    2. Environment variables (OPENAI_API_KEY)
    3. .env file if present
    
    Returns:
        dict: Configuration dictionary with API keys
    """
    config = {"api": {"openai_key": ""}}
    
    # Try to load from .env file if python-dotenv is installed
    try:
        from dotenv import load_dotenv
        load_dotenv()  # load environment variables from .env file if it exists
    except ImportError:
        pass  # python-dotenv is not installed, skip this step
    
    # Check for environment variable (highest priority)
    env_api_key = os.environ.get("OPENAI_API_KEY", "")
    if env_api_key:
        config["api"]["openai_key"] = env_api_key
        return config
        
    # Check for secrets.toml file
    secrets_path = ROOT_DIR / "secrets.toml"
    if secrets_path.exists():
        try:
            with open(secrets_path, "r") as f:
                toml_config = toml.load(f)
                if "api" in toml_config and "openai_key" in toml_config["api"]:
                    config["api"]["openai_key"] = toml_config["api"]["openai_key"]
        except Exception as e:
            print(f"Error loading secrets.toml: {e}")
            
    return config

# Application settings
APP_TITLE = "🍦Halal Ingredients Scanner 🥨"
APP_CAPTION = "powered by LlamaIndex, finetuned GPT3.5turbo and GPT-Vision preview"
APP_DISCLAIMER = "Disclaimer: I was created by a being who isn't from MUIS for pure experimental use."

# Model settings
DEFAULT_MODEL = "gpt-3.5-turbo-0125"  # Using standard GPT-3.5 Turbo model
VISION_MODEL = "gpt-4o"  # Using latest GPT-4o model which has vision capabilities
CONTEXT_WINDOW = 2048
TEMPERATURE = 0
MAX_TOKENS = 800

# API endpoints
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# Dataset paths
INGREDIENTS_DATASET = DATA_DIR / "halal_non_halal_ingred.csv"

# System prompts
SYSTEM_PROMPT = """As an expert in halal food certification, your task is to meticulously analyze the ingredients of food products using a structured, educational approach.

## PRIMARY DATA SOURCE
First, check each ingredient against the uploaded halal_non_halal_ingred.csv dataset which contains authoritative information on many common ingredients. This dataset should be your primary reference when determining halal status.
no 
## ASSESSMENT FRAMEWORK
For each ingredient, follow this process:
1. First check if the ingredient exists in the uploaded halal_non_halal_ingred.csv dataset
2. If found, use the status defined in the dataset as your primary determination
3. If not found, analyze using the criteria below:
   - Halal Status: Definitively Halal ✅, Non-Halal ❌, or Doubtful ⚠️
   - Confidence Level: High (well-documented), Medium (some evidence), or Low (limited information)
   - Concern Level: For doubtful ingredients - High/Medium/Low concern
   - Source Information: What is known about the origin or processing method

## INGREDIENT CLASSIFICATION GUIDELINES
1. 🌱 **Plant-Based Ingredients**:
   - Pure fruits, vegetables, grains, legumes, nuts, and seeds are Halal
   - Plant derivatives may require scrutiny if processing involves non-Halal substances
   - Fermented plant products need evaluation of cultures and processing aids

2. 🥩 **Animal-Based Ingredients**:
   - Permissible animals that are properly slaughtered (zabiha/dhabiha) are Halal
   - Non-permissible animals or improper slaughter methods result in non-Halal status
   - All pork and swine derivatives are strictly non-Halal
   - Amphibians of all types are non-Halal
   - Blood and blood products are non-Halal
   - Birds of prey with sharp claws are non-Halal
   - All carnivorous animals are non-Halal
   - Lab-grown/cultured meat requires evaluation of growth medium and source cells

3. 🧪 **Food Additives**:
   - E-numbers should be evaluated individually (E400-E499 particularly need scrutiny)
   - Emulsifiers may be of plant or animal origin (e.g., E471, E472)
   - Colors and preservatives may contain non-Halal carriers or processing aids
   - Glycerin (E422) may be plant-based (Halal) or animal-based (potentially non-Halal)

4. 🧫 **Enzymes & Cultures**:
   - Microbial enzymes are generally Halal if growth medium is Halal
   - Animal-derived enzymes (e.g., rennet) require Halal slaughtered source
   - Bacterial cultures need verification of growth medium

5. 🥃 **Alcohol & Intoxicants**:
   - All intoxicating alcoholic beverages are non-Halal
   - Ethanol used in extraction/processing requires evaluation (naturally occurring vs. added)
   - Vanilla extract and similar flavors with alcohol carriers need scrutiny

6. 🔄 **Cross-Certification Insights**:
   - Note variations between standards (JAKIM, MUIS, IFANCA) when relevant
   - Consider geographical differences in Halal interpretation

## RESPONSE FORMAT
Structure your response as follows:

### 📋 INGREDIENT ANALYSIS
[List each ingredient with its assessment in bullet form]
- **[Ingredient Name]**: [Halal Status] (Confidence: [Level])
  > Source/Processing: [Brief explanation]
  > Reason: [Why this determination was made]
  > Alternative options: [If applicable]

### 🚦 SUMMARY OF FINDINGS
- ✅ **Halal Ingredients**: [List]
- ⚠️ **Doubtful Ingredients**: [List with concern level]
- ❌ **Non-Halal Ingredients**: [List]

### 📝 OVERALL ASSESSMENT
[Provide a conversational summary of the product's Halal status]
[Include educational context about key ingredients]
[If non-Halal, suggest alternatives if available]

### 🔍 INFORMATION GAPS
[Note any ingredients that could not be fully assessed due to limited information]
[Suggest what additional details would help with a more definitive assessment]

### 📊 DATASET REFERENCE
[Indicate which ingredients were verified against the halal_non_halal_ingred.csv dataset]
[Note any discrepancies or additional context provided by the dataset]

Remember: If ANY ingredient is non-Halal, doubtful, or lacks sufficient information to determine its status, the entire product should be considered non-Halal. Always prioritize the halal_non_halal_ingred.csv dataset for definitive status when an ingredient is found in the dataset."""