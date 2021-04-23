FROM python
COPY chatbot_redis_by_upstash.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=1797928255:AAE8SV6zG-3tSnRTjsFCMKwC0ACcFf0x07k
ENV HOST=redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com
ENV PASSWORD=14af934e50fe40849020d8d22419321d
ENV REDISPORT=30382
CMD ["chatbot_redis_by_upstash.py"]
ENTRYPOINT ["python"]