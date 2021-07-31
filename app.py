import asyncio
import json
from datetime import timedelta

from flask import Flask, render_template

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
app.permanent_session_lifetime = timedelta(seconds=1)
TIME_LIMIT = 3.0001


async def async_get_data(all_result):
    task1 = asyncio.create_task(get_from_file('uploads/file1.json', all_result))
    task2 = asyncio.create_task(get_from_file('uploads/file2.json', all_result))
    task3 = asyncio.create_task(get_from_file('uploads/file3.json', all_result))

    await task1
    await task2
    await task3

    all_result.sort(key=lambda item: int(item.get("id")))

    return all_result


async def get_from_file(file_name, all_result):
    try:
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        all_result.extend(data)
        await asyncio.sleep(TIME_LIMIT)
        return all_result
    except FileNotFoundError:
        return []


@app.route("/")
async def get_data():
    all_result = []

    try:
        await asyncio.wait_for(async_get_data(all_result), timeout=2)
        return render_template('index.html', items=all_result)

    except asyncio.TimeoutError:
        return 'Ошибка! Timeout!'


if __name__ == '__main__':
    app.run(debug=True)
