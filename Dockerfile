FROM python:3.8
RUN useradd -u 1000 -d /app -M -s /bin/false app \
	&& pip install poetry gunicorn
ENV POETRY_VIRTUALENVS_CREATE=false
ENV DEBUG=false

COPY . /app/
WORKDIR /app/
RUN poetry install --no-dev --no-interaction \
	&& python manage.py collectstatic --no-input

RUN chmod +x /app/entrypoint.sh
USER 1000
CMD ["./entrypoint.sh"]