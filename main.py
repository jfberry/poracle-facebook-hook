import asyncio
from aiohttp import web
from aiohttp import ClientSession
import fbchat
import configparser


async def post(request):
    session = request.app['session']
    client = request.app['client']

    name = request.match_info.get('channel', "Anonymous")

    print("Posting to: {}".format(name))
    message = None
    image = None
    location = None
    thumbnail = None
    if request.can_read_body:
        js = await request.json()

        if "content" in js:
            message = js["content"]

        if "embeds" in js:
            message = js["embeds"][0]["title"]
            message += "\n" + js["embeds"][0]["description"]
            if "image" in js["embeds"]:
                image = js["embeds"][0]["image"]["url"]
            if "thumbnail" in js["embeds"]:
                thumbnail = js["embeds"][0]["thumbnail"]["url"]

        if "location" in js:
            lat = js["location"]["latitude"]
            lon = js["location"]["longitude"]
            location = {'latitude': lat, 'longitude': lon}

    asyncio.create_task(post_message(session, client, name, message, image, location))

    return web.Response(text="OK")


async def post_message(session, client, id, message, image, location):
    thread = fbchat.Group(session=session, id=id)

    if message is not None:
        await thread.send_text(message)

    if image is not None:
        async with ClientSession() as sess, sess.get(image) as resp:
            image_data = await resp.read()
            files = await client.upload([("image_name.png", image_data, "image/png")])
            await thread.send_files(files)  # Alternative to .send_text

    if location is not None:
        await thread.send_pinned_location(location["latitude"], location["longitude"])


async def init_app(user, password):

    app = web.Application()
    session = await fbchat.Session.login(user, password)
    client = fbchat.Client(session=session)

    app['session'] = session
    app['client'] = client

    app.add_routes([web.post('/{channel}', post)])

    return app

config = configparser.ConfigParser()
config.read('config.ini')

user = config['main']['user']
password = config['main']['password']
port = config['main']['port']

web.run_app(init_app(user, password), port=port)

# Log the user out
# await session.logout()
