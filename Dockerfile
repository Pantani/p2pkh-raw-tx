FROM python:3.7

COPY . /home
WORKDIR /home

RUN make install-packages
RUN make install-test-packages
RUN make test
RUN make clean

EXPOSE 5000

CMD make run
