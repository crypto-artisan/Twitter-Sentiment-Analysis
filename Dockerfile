FROM python:3.9-slim

# Maintainer info
LABEL maintainer="mario.novella@gmail.com"

# Make working directories
RUN  mkdir -p  /sentiment-analisis-api
WORKDIR  /sentiment-analisis-api

# Upgrade pip with no cache
RUN pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY  . .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory


ENV PORT=8000
EXPOSE 8000

# Run the python application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]