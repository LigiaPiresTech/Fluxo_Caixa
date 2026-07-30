FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY shared ${LAMBDA_TASK_ROOT}/shared
COPY api_usuarios ${LAMBDA_TASK_ROOT}/api_usuarios
COPY api_cadastros ${LAMBDA_TASK_ROOT}/api_cadastros
COPY api_contas ${LAMBDA_TASK_ROOT}/api_contas
COPY api_lancamentos ${LAMBDA_TASK_ROOT}/api_lancamentos
COPY api_consolidado ${LAMBDA_TASK_ROOT}/api_consolidado
COPY api_relatorios ${LAMBDA_TASK_ROOT}/api_relatorios

CMD ["api_lancamentos.handler.handler"]
