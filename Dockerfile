# -----------------------------
# 1️⃣ Base image
# -----------------------------
FROM python:3.13-slim

# -----------------------------
# 2️⃣ Working directory inside container
# -----------------------------
WORKDIR /app

# -----------------------------
# 3️⃣ Copy dependency list & install
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 4️⃣ Copy project files
# -----------------------------
COPY . .

# -----------------------------
# 5️⃣ Set environment variables
# -----------------------------
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# -----------------------------
# 6️⃣ Expose port 5000
# -----------------------------
EXPOSE 5011

# -----------------------------
# 7️⃣ Command to start Flask
# -----------------------------
CMD ["python", "run.py"]
