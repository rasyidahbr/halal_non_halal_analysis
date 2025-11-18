# Halal Ingredient Analysis

An intelligent application that analyzes food ingredients to determine if they are halal, non-halal, or doubtful using advanced AI techniques.

## Background

In an increasingly diverse and globalized food market, ensuring that individuals with specific dietary requirements, such as those adhering to Halal principles, can confidently identify suitable food products remains a significant challenge. This application helps Muslim consumers make informed choices by analyzing ingredient lists from product images or through chat interactions.

## Features

- **Image Analysis**: Upload images of product labels to extract and analyze ingredients
- **Ingredient Classification**: Determine if ingredients are halal, non-halal, or doubtful
- **AI-Powered Chat**: Ask questions about halal status of specific ingredients
- **Export Results**: Save analysis results for later reference
- **Detailed Explanations**: Get explanations for ingredient classifications
- **User-Friendly Interface**: Clean and intuitive Streamlit interface

## Project Structure

```
halal_non_halal_analysis/
│
├── app_improved.py         # Main application entry point
├── app.py                  # Original application (for reference)
├── config/                 # Configuration files
│   └── settings.py         # Application settings and constants
│
├── src/                    # Source code modules
│   ├── api/                # API integration modules
│   │   ├── llama_index_handler.py  # LlamaIndex operations
│   │   └── openai_handler.py       # OpenAI API integration
│   │
│   ├── ui/                 # UI components
│   │   └── components.py   # Streamlit UI components
│   │
│   └── utils/              # Utility modules
│       ├── data_handler.py  # Data loading and processing
│       └── ingredient_parser.py  # Ingredient text parsing
│
├── data/                   # Data files
│   └── halal_non_halal_ingred.csv  # Ingredient database
│
├── storage/                # LlamaIndex storage
├── assets/                 # Application assets
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/rasyidahbr/halal_non_halal_analysis.git
   cd halal_non_halal_analysis
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key (choose one method):
   
   **Option A: Using a .env file**
   - Copy the template file:
     ```
     cp .env.template .env
     ```
   - Edit the `.env` file and add your OpenAI API key
   
   **Option B: Using environment variables**
   - Set the environment variable directly:
     ```
     # On Windows
     set OPENAI_API_KEY=your-openai-api-key
     
     # On macOS/Linux
     export OPENAI_API_KEY=your-openai-api-key
     ```
   
   **Option C: Using secrets.toml**
   - Create a `secrets.toml` file in the root directory:
     ```
     [api]
     openai_key = "your-openai-api-key"
     ```

4. Run the application:
   ```
   streamlit run app_improved.py
   ```

## Usage

### Image Analysis
1. Upload an image of a product label
2. The application will extract ingredients from the image
3. The ingredients will be classified as halal, non-halal, or doubtful
4. Unknown ingredients will be analyzed using OpenAI
5. Results can be exported for later reference

### Chat Interface
1. Type a question about halal ingredients
2. The application will search its knowledge base
3. Get detailed answers about specific ingredients or general halal guidelines

## Data Sources

- The halal food data utilized is sourced from the MUIS website
- Additional sources include World of Islam Food Numbers and Islamcan.com
- A fine-tuned GPT-3.5-Turbo model enhances the accuracy of responses

## Future Improvements

- Batch processing of multiple images
- Multi-language support for ingredients in different languages
- Mobile app version for on-the-go use
- Community contribution for expanding the ingredient database
- Offline mode for use without internet connection

## Credits

Developed by Rasyidah B R

## License

This project is licensed under the MIT License