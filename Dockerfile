FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so they are cached between image builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code and sample data.
COPY src/ src/
COPY data/ data/

ENTRYPOINT ["python", "src/main.py"]
CMD ["--demo"]
