FROM amazonlinux

RUN yum update -y && \
    yum install -y python3 pip3

# Copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 80

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
