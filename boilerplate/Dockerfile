FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app
COPY ./models /models

RUN pip install fastapi redis sqlalchemy pydantic

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

