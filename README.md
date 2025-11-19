
# Halal Ingredient Analysis

An intelligent application that analyzes food ingredients to determine if they are halal, non-halal, or doubtful using advanced AI techniques and a comprehensive ingredient database.

## Background

In an increasingly diverse and globalized food market, ensuring that individuals with specific dietary requirements, such as those adhering to Halal principles, can confidently identify suitable food products remains a significant challenge. This application helps Muslim consumers make informed choices by analyzing ingredient lists from product images or through interactive chat.

## Features

- **🖼️ Image Analysis**: Upload product label images to extract and analyze ingredients using OCR
- **🔍 Ingredient Classification**: Determine if ingredients are halal, non-halal, or doubtful based on comprehensive database
- **🤖 AI-Powered Chat**: Ask questions about halal status of specific ingredients using OpenAI GPT
- **📊 Export Results**: Save analysis results as CSV for later reference
- **💬 Detailed Explanations**: Get explanations for ingredient classifications and doubtful cases
- **🎨 User-Friendly Interface**: Clean and intuitive Streamlit interface with modern design
- **🔄 Multiple Processing Options**: Choose between local database lookup and AI analysis

## Problem Statement

Accessing accurate Halal product information is challenging, hindering Muslim consumers' dietary choices. This project provides an automated system that analyzes ingredient lists from product images to determine their Halal status, offering a convenient solution for Halal-conscious consumers worldwide.

## Objective

- Create an intelligent system that can classify food products as halal, not halal, or uncertain based on their ingredient lists
- Provide real-time analysis using both database lookup and AI-powered assessment
- Enhance the ability of consumers, especially Muslims, to make informed choices when purchasing food items abroad
- Offer educational insights about ingredient classifications and Halal principles
## Success Metrics

- **Answer Relevancy**: Measures how relevant the generated answer is to the user's question
- **Faithfulness**: Measures the accuracy of the generated answer and prevents hallucination
- **User Experience**: Intuitive interface with clear results and explanations
- **Processing Speed**: Fast analysis for both image processing and chat responses

## Project Structure

```
halal_non_halal_analysis/
│
├── app_improved.py         # Enhanced main application with modern UI
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
│   └── halal_non_halal_ingred.csv  # Comprehensive ingredient database
│
├── storage/                # LlamaIndex storage for document indexing
├── assets/                 # Application assets (images, etc.)
├── requirements.txt        # Project dependencies
├── Dockerfile             # Docker containerization
├── .env.template          # Environment variables template
└── setup.py              # Package installation script
```

## Installation & Setup

### Option 1: Local Installation

1. **Clone the repository**:
```bash
git clone https://github.com/rasyidahbr/halal_non_halal_analysis.git
cd halal_non_halal_analysis
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.template .env
# Edit .env file with your OpenAI API key
```

4. **Run the application**:
```bash
streamlit run app_improved.py
```

### Option 2: Docker Installation

1. **Build the Docker image**:
```bash
docker build -t halal-analysis .
```

2. **Run the container**:
```bash
docker run -p 8501:8501 halal-analysis
```

### Option 3: Quick Start (Windows)
```bash
# Run the batch file for quick setup
run_app.bat
```
## Data

- The halal food data utilized is sourced from the MUIS website, and this information is also employed in the backend processing of GPT 3.5 Turbo.
    - [MUIS: Food and Drinks Categories](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-and-Drinks-Categories)
    - [MUIS: Food Selection](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-Selection)
    - [MUIS: Food Preparation](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-Preparation)    


- the `halal_non_halal_ingred.csv` ingredient list is consolidated from:-
    - [MUIS: Food Additive List](https://www.muis.gov.sg/-/media/Files/Halal/Documents/FOOD-ADDITIVE-LISTING-5.ashx)
    - [World of Islam Food Numbers](https://special.worldofislam.info/Food/numbers.html)
    - [Islamcan.com](https://islamcan.com/blog/2020/01/halal-and-haram-ingredient-database/)

### Data Dictionary

| Column Name               | Description                                                                                               |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| `ingred_name`             | Code or short identifier for each ingredient.                                                             |
| `chem_name`               | The chemical name of the ingredient.                                                                      |
| `description`             | A brief description of the ingredient, indicating its use or properties.                                 |
| `halal_non_halal_doubtful` | Numerical value indicating the halal status: 0 for Halal, 1 for Non-Halal, 2 for Doubtful.               |

## How It Works

### 🖼️ Image Analysis Workflow
1. **Image Upload**: Users upload product label images through the web interface
2. **OCR Processing**: Advanced text extraction identifies ingredients from the image
3. **Ingredient Parsing**: Smart parsing separates individual ingredients from complex lists
4. **Database Lookup**: Cross-reference ingredients with comprehensive halal/non-halal database
5. **AI Analysis**: For unknown ingredients, use OpenAI GPT for intelligent classification
6. **Results Display**: Clear presentation of findings with explanations and export options

### 💬 Chat Interface Workflow
1. **Question Input**: Users ask specific questions about ingredient halal status
2. **Context Understanding**: AI processes the query using fine-tuned models
3. **Knowledge Retrieval**: Access indexed halal food guidelines and regulations
4. **Intelligent Response**: Generate accurate answers based on Islamic dietary laws
5. **Educational Content**: Provide additional context and explanations

### 🔄 Processing Options
- **Fast Mode**: Quick database lookup for known ingredients
- **Comprehensive Mode**: AI-powered analysis for complex or unknown ingredients
- **Hybrid Mode**: Combines both approaches for optimal accuracy
## Results & Performance

### ✅ Key Achievements
- **High Accuracy**: Effective identification of basic ingredients with 96.8% answer relevancy
- **Reliable AI**: GPT-3.5-turbo-1106 model with 80% faithfulness score
- **User-Friendly**: Intuitive interface with clear visual feedback
- **Comprehensive Coverage**: Handles both common and obscure ingredients
- **Educational Value**: Provides explanations for ingredient classifications

### 📊 Model Performance
- **Answer Relevancy**: 0.968 (96.8%)
- **Faithfulness**: 0.8 (80%)
- **Model**: GPT-3.5-turbo-1106 (optimal performance)
- **Processing Speed**: < 3 seconds average response time

### 🎯 Use Cases
- **Travelers**: Quick ingredient checks while shopping abroad
- **Families**: Verify children's snacks and meals
- **Restaurants**: Staff training on halal ingredient identification
- **Food Manufacturers**: Quality assurance for halal certification
- **Students**: Learning about Islamic dietary laws

## Future Enhancements

### 🚀 Planned Features
- **Multi-language Support**: Support for Arabic, Malay, and other languages
- **Offline Mode**: Local processing without internet dependency
- **Mobile App**: Native iOS and Android applications
- **Barcode Scanner**: Direct product lookup via barcode
- **Community Features**: User reviews and crowdsourced ingredient data

### 🔧 Technical Improvements
- **Enhanced OCR**: Better recognition of complex ingredient lists
- **Sub-ingredient Analysis**: Detailed breakdown of compound ingredients
- **Real-time Processing**: Faster image analysis and AI responses
- **Custom Training**: Domain-specific model fine-tuning
- **API Integration**: Connect with major food databases




## Repository Contents

### 🚀 Main Applications
- **[app_improved.py](app_improved.py)** - Enhanced main application with modern UI and improved features
- **[app.py](app.py)** - Original application (maintained for reference and compatibility)

### 📁 Core Modules
- **[src/](src/)** - Organized source code with modular architecture:
  - `api/` - API integration handlers (OpenAI, LlamaIndex)
  - `ui/` - User interface components and layouts
  - `utils/` - Utility functions for data processing and parsing

### 🛠️ Configuration & Setup
- **[config/settings.py](config/settings.py)** - Application configuration and constants
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[Dockerfile](Dockerfile)** - Container configuration for deployment
- **[setup.py](setup.py)** - Package installation script
- **[run_app.bat](run_app.bat)** - Quick start script for Windows

### 📊 Data & Processing
- **[backend_processing.ipynb](backend_processing.ipynb)** - Backend data processing and model preparation
- **[final_gpt.ipynb](final_gpt.ipynb)** - Main workflow demonstration and testing
- **[EDA.ipynb](EDA.ipynb)** - Exploratory data analysis of ingredient database

### 📈 Analysis & Evaluation
- **[df_gpt_35.csv](df_gpt_35.csv)** - Performance scores and evaluation metrics
- **[train_questions.txt](train_questions.txt)** - Training dataset for model fine-tuning
- **[eval_questions.txt](eval_questions.txt)** - Evaluation questions for testing
- **[finetuning_events.jsonl](finetuning_events.jsonl)** - Fine-tuning events and logs

### 📖 Documentation & Resources
- **[slides/](slides/)** - Presentation materials in multiple formats
- **[data/](data/)** - Comprehensive ingredient database and reference materials
- **[storage/](storage/)** - LlamaIndex document storage and indexing
- **[assets/](assets/)** - Application assets and sample images

### 📋 Additional Processing Files
- **[cd/](cd/)** - Preprocessing files for ingredient database conversion
- **[task/](task/)** - Task-oriented processing experiments and results

## Contributing

We welcome contributions! Please feel free to:
1. **Report Issues**: Submit bug reports or feature requests
2. **Improve Documentation**: Help enhance our guides and explanations
3. **Add Ingredients**: Contribute to our ingredient database
4. **Test Features**: Help test new functionality across different devices
5. **Translate Content**: Support multi-language features

## License

This project is open-source and available under the MIT License.

## Acknowledgments

- **MUIS (Majlis Ugama Islam Singapura)** for halal food guidelines and regulations
- **OpenAI** for GPT API access and AI capabilities
- **Streamlit** for the web application framework
- **Community Contributors** for ingredient data and feedback

## Contact & Support

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check our comprehensive guides and examples
- **Community**: Join our discussions and share your experiences

---

**Made with ❤️ for the Muslim community worldwide** 🌍
