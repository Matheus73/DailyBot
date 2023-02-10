FROM python:3.10

ENV TZ=America/Sao_Paulo

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src/main.py .
COPY ./src/table.md .

CMD python main.py