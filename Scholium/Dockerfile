FROM python:3.12


WORKDIR /ScholiumModel


COPY ./requirements.txt ./


RUN pip install --no-cache-dir -r ./requirements.txt


COPY . . 


CMD ["fastapi", "run", "server.py"]

