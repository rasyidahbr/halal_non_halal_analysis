FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the assets directory exists
RUN mkdir -p assets

# Make port 8501 available to the world outside the container
EXPOSE 8501

# Define environment variable for OpenAI API key (should be provided at runtime)
ENV OPENAI_API_KEY=""

# Run the application
CMD ["streamlit", "run", "app_improved.py", "--server.port=8501", "--server.address=0.0.0.0"]