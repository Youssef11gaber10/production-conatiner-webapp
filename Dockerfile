# FROM python:3.11-slim as builder 

# WORKDIR /app

# COPY ./requirements.txt .

# # RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# # ------------ Stage 2 ------------

# FROM  python:3.11-alpine

# WORKDIR /app

# RUN apk update && apk add --no-cache gcc musl-dev libpq postgresql-dev


# COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# COPY --from=builder /usr/local/bin /usr/local/bin

# COPY . .

# EXPOSE 5000

# CMD ["python", "app/main.py"]






# FROM python:3.9.22-bullseye AS builder

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# FROM python:3.9.22-slim-bullseye

# WORKDIR /app

# COPY --from=builder /usr/local /usr/local

# COPY --from=builder /app /app

# EXPOSE 80

# CMD ["python", "app/main.py"]



FROM python:3.11-slim
WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

COPY . . 


CMD ["python", "app/main.py"]
