FROM python:3.9

WORKDIR /narzedzia-projekt

COPY . /narzedzia-projekt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]