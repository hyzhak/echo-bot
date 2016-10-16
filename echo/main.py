import asyncio
import botstory
from botstory import chat, story
from botstory.integrations import aiohttp, fb, mongodb
from botstory.middlewares import any, text
import logging
import os

logger = logging.getLogger('echo-bot')
logger.setLevel(logging.DEBUG)


# define stories

@story.on(receive=text.Any())
def echo_story():
    @story.part()
    async def echo(message):
        await chat.say('Hi! I just got something from you:', message['user'])
        await chat.say('> {}'.format(message['data']['text']['raw']), message['user'])


@story.on(receive=any.Any())
def else_story():
    @story.part()
    async def something_else():
        await chat.say('Hm I don''t know what is it')


# setup modules

async def init(fake_http_session=None):
    story.use(fb.FBInterface(
        token=os.environ.get('FB_ACCESS_TOKEN', None),
        webhook=os.environ.get('WEBHOOK_URL_SECRET_PART', '/webhook'),
    ))
    story.use(aiohttp.AioHttpInterface(
        port=os.environ.get('API_PORT', 8080),
    )).session = fake_http_session
    db = story.use(mongodb.MongodbInterface(
        uri='mongo',
        db_name='tests',
    ))

    await story.start()
    logger.info('start!')


async def stop():
    await botstory.story.stop()


# launch app

def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())

    story.forever(loop)

    # TODO: 1) we should support gunicorn


if __name__ == '__main__':
    main()
