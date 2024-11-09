FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install the graphedexcel package
RUN pip install graphedexcel -U

# Copy the rest of the application code
#COPY . .

# Set the entry point to call graphedexcel
ENTRYPOINT ["python", "-m", "graphedexcel"]
