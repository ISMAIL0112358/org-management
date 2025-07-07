FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y gcc libpq-dev && \
 pip install fastapi uvicorn pydantic passlib[bcrypt] python-multipart pyjwt psycopg2
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]