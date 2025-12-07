FROM python:3.12

RUN apt update && apt install -y make pandoc libreoffice
RUN pip install --upgrade pip && pip install uv

COPY . /docx
WORKDIR /docx
RUN make install

CMD ["make", "serve"]
