import asyncio
import json

from flask import Flask


app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

ALL_RESULT = []
TIME_LIMIT = 0.1


async def async_get_data(file_name):
    data = get_from_file(file_name)
    ALL_RESULT.extend(data)
    await asyncio.sleep(TIME_LIMIT)
    return ALL_RESULT


def get_from_file(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        return data


@app.route("/")
async def get_data():

        task1 = asyncio.create_task(async_get_data('uploads/file1.json'))
        task2 = asyncio.create_task(async_get_data('uploads/file2.json'))
        task3 = asyncio.create_task(async_get_data('uploads/file3.json'))

        await task1
        await task2
        await task3

        ALL_RESULT.sort(key=lambda item: int(item.get("id")))
        return json.dumps(ALL_RESULT)


if __name__ == '__main__':
    app.run(debug=True)
