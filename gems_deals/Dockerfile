FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY ./ .

CMD ["gunicorn", "gems_deals.wsgi:application", "--bind", "0:8000"]

LABEL author='4kolesov@gmail.com' version=0.1
