FROM ubuntu
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install uvicorn
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app"]
