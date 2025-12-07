FROM python:3.12

RUN apt update && apt install -y make
RUN pip install --upgrade pip && pip install uv

COPY . /xlsx
WORKDIR /xlsx
RUN make install

CMD ["make", "serve"]
