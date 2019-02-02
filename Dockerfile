FROM python:3.6.0
RUN mkdir /files


ADD requirements /requirements/
ADD manage.py /
RUN pip install -r /requirements/production.txt

WORKDIR /files/
COPY ./entrypoint.sh /files/entrypoint.sh
CMD ["bash", "/files/entrypoint.sh"]

