FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
COPY *.py /home/
COPY templates/*.* /home/templates/
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["python3","/home/catalogue.py" ]
