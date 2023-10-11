FROM ubuntu
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install requirements
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install uvicorn
COPY . .
RUN pip install -r requirements.txt
EXPOSE 443
CMD uvicorn server:app --workers 1 --host 0.0.0.0 --port 443
