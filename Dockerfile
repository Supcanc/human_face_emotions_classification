FROM python:3.14

WORKDIR /workdir

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "server/app.py" ]