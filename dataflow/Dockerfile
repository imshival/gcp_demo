FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN apt-get update && apt-get install -y libffi-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY dataflow.py .

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/dataflow.py"

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
RUN pip install apache-beam[gcp]
RUN pip install -U -r ./requirements.txt