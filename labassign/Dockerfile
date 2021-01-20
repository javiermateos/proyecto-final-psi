# Base image
FROM python:3.6

# Maintainer
LABEL Author="Javier"

# The environment variable ensures that they paython output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Switch to app directory so that everything runs from here
WORKDIR /code

# Copy the requirements to the image working directory
COPY requirements.txt /code/

# Let pip install required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 


# Copy de app code to the image working directory
COPY . /code/

RUN apt update && apt install netcat-traditional

ENTRYPOINT ["/code/entrypoint.sh"]
