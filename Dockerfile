FROM python:3.9

RUN mkdir midata
WORKDIR /midata

COPY requirements.txt requirements.txt
COPY run.sh /midata
ADD  mysayhello /midata

RUN pip3 install -r requirements.txt

COPY . .

CMD ["/midata/run.sh"]
# CMD ["flask","forge"]
# CMD ['Flask', "run"]