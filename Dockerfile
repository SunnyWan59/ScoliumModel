# FROM python:3.12 AS builder
# WORKDIR /ScholiumModel

# RUN python3 -m venv venv
# ENV VIRTUAL_ENV=/ScholiumModel/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# # Install the application dependencies
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install uvicorn
# RUN pip install "fastapi[standard]"
 
# # Stage 2
# FROM python:3.12 AS runner
 
# WORKDIR /ScholiumModel
 
# COPY --from=builder /ScholiumModel/venv venv
# COPY main.py main.py

# COPY . .

# ENV VIRTUAL_ENV=/app/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
# EXPOSE 8000
 
# CMD [ "uvicorn", "--host", "0.0.0.0", "main:app"]\
# CMD ["python", "-V"]
# CMD ["fastapi", "run", "main.py"]

FROM python:3.12


WORKDIR /ScholiumModel


COPY ./requirements.txt ./


RUN pip install --no-cache-dir -r ./requirements.txt


COPY . . 


CMD ["fastapi", "run", "main.py"]

