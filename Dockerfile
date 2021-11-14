FROM python:latest
RUN mkdir movieapp/
COPY . /movieapp
WORKDIR /movieapp/
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]