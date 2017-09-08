FROM python:3

COPY . .
RUN pip3 install -r requirements.txt

# non-root user
RUN groupadd -r python && \
    useradd -r -M -g python python
USER python

CMD python app.py
