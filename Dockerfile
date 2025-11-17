FROM python:3.12-slim AS builder

# dependencies
ENV PATH=/root/.local/bin:/usr/local/bin/:/usr/sbin:/usr/bin:/sbin:/bin
ENV PDM_CHECK_UPDATE=false
RUN pip install -U pdm
WORKDIR /app

# things that are the biggest and not likely to change too often
COPY pyproject.toml pdm.lock README.md /app/
# --mount=type=cache,target=/app/.venv not usable because it doesn't mount in prod apparently
RUN pdm install --check --prod --no-editable

##### END BUILDER PHASE #####

FROM --platform=$BUILDPLATFORM python:3.12-slim

ENV PATH=/app/.venv/bin:/root/.local/bin:/usr/local/bin/:/usr/sbin:/usr/bin:/sbin:/bin
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . /app

CMD gunicorn library_app:app -w $(nproc) -b [::]

LABEL org.opencontainers.image.authors="me@soopy.moe"
