from core.celery import celery


@celery.task()
def ping():
    print("ECHO")


@celery.task()
def long_ping():
    from asyncio import run

    async def task():
        print("LONG PING")

    run(task())
