FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
RUN useradd -r -u 10001 appuser && chown -R appuser /app
USER appuser
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
