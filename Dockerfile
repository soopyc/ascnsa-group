FROM --platform=$BUILDPLATFORM python:3.12-slim AS builder

# dependencies
WORKDIR /build
ENV PATH=/root/.local/bin:/usr/local/bin/:/usr/sbin:/usr/bin:/sbin:/bin
ENV PDM_CHECK_UPDATE=false
RUN pip install -U pdm

# things that are the biggest and not likely to change too often
COPY pyproject.toml pdm.lock README.md /build
RUN --mount=type=cache,target=/app/.venv pdm install --check --prod --no-editable

##### END BUILDER PHASE #####

FROM --platform=$BUILDPLATFORM python:3.12-slim
ENV PATH=/root/.local/bin:/usr/local/bin/:/usr/sbin:/usr/bin:/sbin:/bin

COPY --from=builder /build/.venv /app/.venv
COPY . /app

CMD ["gunicorn", "app:app", "-w", "4"]
