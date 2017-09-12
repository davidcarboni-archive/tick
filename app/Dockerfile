FROM python:3

# Add requirements first so this layer can be cached:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add code
COPY . .

# Switch to a non-root user
RUN groupadd -r python && \
    useradd -r -M -g python python
USER python

# Go!
CMD python app.py
