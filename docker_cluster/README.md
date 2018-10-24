# Scheduled task

To run scheduled tasks you need broker for celery

```
docker run -d \
    --name="rabbit1" \
    --hostname="rabbit1"\
    -e RABBITMQ_ERLANG_COOKIE="secret string" \
    -e RABBITMQ_NODENAME="rabbit1" \
    --volume=(pwd)/rabbitmq.config:/etc/rabbitmq/rabbitmq.config \
    --volume=(pwd)/definitions.json:/etc/rabbitmq/definitions.json \
    --publish="4369:4369" \
    --publish="5671:5671" \
    --publish="5672:5672" \
    --publish="15671:15671" \
    --publish="15672:15672" \
    --publish="25672:25672" \
    rabbitmq:latest
```
```
docker run -d \
    --name="rabbit2" \
    --hostname="rabbit2"\
    -e RABBITMQ_ERLANG_COOKIE="secret string" \
    -e RABBITMQ_NODENAME="rabbit2" \
    --volume=(pwd)/rabbitmq.config:/etc/rabbitmq/rabbitmq.config \
    --volume=(pwd)/definitions.json:/etc/rabbitmq/definitions.json \
    --link="rabbit1:rabbit1" \
    rabbitmq:latest
```
```
docker run -d \
    --name="rabbit3" \
    --hostname="rabbit3"\
    -e RABBITMQ_ERLANG_COOKIE="secret string" \
    -e RABBITMQ_NODENAME="rabbit3" \
    --volume=(pwd)/rabbitmq.config:/etc/rabbitmq/rabbitmq.config \
    --volume=(pwd)/definitions.json:/etc/rabbitmq/definitions.json \
    --link="rabbit1:rabbit1" \
    --link="rabbit2:rabbit2" \
    rabbitmq:latest
```
You can use this containers.
```
docker stop rabbit1 rabbit2 rabbit3
```
```
docker start rabbit1 rabbit2 rabbit3
```
Now you can run celery worker. Change working directory to `pytatki/docker_cluster/test_celery`
```
celery -A tasks.app worker --loglevel=info
```
Run flask test app
```
python3 tasks.py
```