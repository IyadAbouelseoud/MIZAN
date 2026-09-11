# Shared image for the `twin` and `api` services (Stage 0). Dependency layer is cached:
# only pyproject.toml is copied before `pip install`, so source edits do not reinstall deps.
FROM python:3.11.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    JAX_PLATFORMS=cpu

WORKDIR /app

# 1. dependencies (cached until pyproject.toml changes)
COPY pyproject.toml ./
RUN python -c "import tomllib; p = tomllib.load(open('pyproject.toml', 'rb'))['project']; open('/tmp/requirements.txt', 'w').write(chr(10).join(p['dependencies'] + p['optional-dependencies']['dev']))" \
 && pip install -q --no-cache-dir -r /tmp/requirements.txt

# 2. source (changes often, cheap layer)
COPY . .

EXPOSE 8000
CMD ["uvicorn", "packages.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
