#!/bin/bash

# 1. Força a criação e coleta dos arquivos estáticos na inicialização
echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

# 2. Liga o servidor do Gunicorn apontando para o seu projeto
echo "=== Iniciando o Gunicorn ==="
gunicorn --bind 0.0.0.0:8000 --workers 2 config.wsgi:application