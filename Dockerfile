FROM ubuntu
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install uvicorn
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "server:app"]
