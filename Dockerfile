FROM python:3.14

WORKDIR /workdir

COPY . .

RUN pip install torch==2.9.1+cu130 torchvision==0.24.1+cu130 --index-url https://download.pytorch.org/whl/cu130

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "api/app.py" ]