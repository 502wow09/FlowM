FROM python:2.8.2
RUN mkdir movieapp/
COPY . /movieapp
WORKDIR /movieapp/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "manage.py", "runserver"]