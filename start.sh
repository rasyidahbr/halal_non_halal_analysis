#!/bin/bash
streamlit run app_streamlit.py --server.port=${PORT:-8080} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false