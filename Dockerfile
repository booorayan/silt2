FROM python:3.10

RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential

WORKDIR /app

COPY . .

ARG SECRET_KEY
ARG OIDC_RP_SIGN_ALGO
ARG OIDC_OP_JWKS_ENDPOINT
ARG OIDC_RP_CLIENT_ID
ARG OIDC_RP_CLIENT_SECRET
ARG OIDC_OP_AUTHORIZATION_ENDPOINT
ARG OIDC_OP_TOKEN_ENDPOINT
ARG OIDC_OP_USER_ENDPOINT
ARG OIDC_CALLBACK_PUBLIC_URI
ARG AFRICASTALKING_API_KEY

ENV SECRET_KEY=$SECRET_KEY
ENV OIDC_RP_SIGN_ALGO=$OIDC_RP_SIGN_ALGO
ENV OIDC_OP_JWKS_ENDPOINT=$OIDC_OP_JWKS_ENDPOINT
ENV OIDC_RP_CLIENT_ID=$OIDC_RP_CLIENT_ID
ENV OIDC_RP_CLIENT_SECRET=$OIDC_RP_CLIENT_SECRET
ENV OIDC_OP_AUTHORIZATION_ENDPOINT=$OIDC_OP_AUTHORIZATION_ENDPOINT
ENV OIDC_OP_TOKEN_ENDPOINT=$OIDC_OP_TOKEN_ENDPOINT
ENV OIDC_OP_USER_ENDPOINT=$OIDC_OP_USER_ENDPOINT
ENV OIDC_CALLBACK_PUBLIC_URI=$OIDC_CALLBACK_PUBLIC_URI
ENV AFRICASTALKING_API_KEY=$AFRICASTALKING_API_KEY

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
