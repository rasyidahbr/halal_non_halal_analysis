# Streamlit Deployment Guide

## Quick Deploy to Streamlit Cloud

1. **Visit Streamlit Cloud**: Go to https://share.streamlit.io/
2. **Sign in with GitHub**: Use your GitHub account
3. **Deploy new app**: 
   - Repository: `rasyidahbr/halal_non_halal_analysis`
   - Branch: `main` 
   - Main file path: `app_improved.py`
4. **Add secrets**: In Advanced settings, add your OpenAI API key
5. **Deploy**: Click "Deploy!"

Your app will be live at: `https://[app-name].streamlit.app`

## Environment Variables Needed

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Local Testing

```bash
streamlit run app_improved.py
```