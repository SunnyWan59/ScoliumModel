FROM python:3.12 as builder
WORKDIR /ScholiumModel

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/ScholiumModel/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

 
# Stage 2
FROM python:3.12 AS runner
 
WORKDIR /ScholiumModel
 
COPY --from=builder /ScholiumModel/venv venv
COPY main.py main.py
 
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
EXPOSE 8000
 
CMD [ "uvicorn", "--host", "0.0.0.0", "main:app" ]