FROM python:3.8-alpine
RUN /usr/local/bin/python -m pip install --upgrade pip
ADD . /shifts
WORKDIR /shifts
RUN pip install -r requirements.txt
CMD flask run
