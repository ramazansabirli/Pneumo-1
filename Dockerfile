# ---- Base image ----
FROM python:3.10-slim

# ---- Environment setup ----
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Port exposure ----
EXPOSE 10000

# ---- Start command ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
