FROM python:3.12-slim

WORKDIR /work

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /work/
RUN pip install --no-cache-dir -r requirements.txt

COPY .. /work/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

