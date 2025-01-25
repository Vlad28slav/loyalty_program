FROM python:3.12

COPY . /code

WORKDIR /code

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]