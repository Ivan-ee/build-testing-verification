FROM python:3.12

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "recipe_project.wsgi:application", "-b", "0.0.0.0:8000", "-w", "3", "-t", "30"]