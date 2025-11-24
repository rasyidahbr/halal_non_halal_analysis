# Streamlit Deployment Guide

## Quick Deploy to Streamlit Cloud

### Option 1: Simple App (Recommended for first deployment)
1. **Visit Streamlit Cloud**: Go to https://share.streamlit.io/
2. **Sign in with GitHub**: Use your GitHub account
3. **Deploy new app**: 
   - Repository: `rasyidahbr/halal_non_halal_analysis`
   - Branch: `main` 
   - Main file path: `app_simple.py`
4. **Deploy**: Click "Deploy!"

### Option 2: Full Featured App (requires OpenAI API)
1. **Visit Streamlit Cloud**: Go to https://share.streamlit.io/
2. **Sign in with GitHub**: Use your GitHub account
3. **Deploy new app**: 
   - Repository: `rasyidahbr/halal_non_halal_analysis`
   - Branch: `main` 
   - Main file path: `app_improved.py`
4. **Add secrets**: In Advanced settings, add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```
5. **Deploy**: Click "Deploy!"

Your app will be live at: `https://[app-name].streamlit.app`

## Troubleshooting Common Errors

### "Unexpected error" during deployment:
- Try using `app_simple.py` instead of `app_improved.py`
- Check that all files are properly committed to GitHub
- Ensure requirements.txt has compatible versions

### "Module not found" errors:
- Verify all dependencies are listed in requirements.txt
- Try the simple app first, then upgrade to full app

### "Import errors":
- Use the simplified app_simple.py for basic functionality
- Add API keys only after basic deployment works

## Local Testing

```bash
streamlit run app_improved.py
```