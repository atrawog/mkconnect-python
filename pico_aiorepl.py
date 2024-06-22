# install aiorepl-lib first!
# to install in VSCode use command "micropico-device-wifi.focus" of VSCode-extension MicroPico
# connect to WiFi and install package "aiorepl"

import asyncio
import aiorepl
import logging

logger = logging.getLogger(__name__)

state = 20
t1Task: asyncio.Task | None = None
replTask: asyncio.Task | None = None
mainTask: asyncio.Task | None = None

def exit():
    print("exit demo")
    state = 0
    if(t1Task is not None):
        t1Task.cancel()
    if(replTask is not None):
        replTask.cancel()
    if(mainTask is not None):
        mainTask.cancel()

async def task1():
    import consoletest
    while state:
        #print("task 1")
        await asyncio.sleep_ms(500)
    print("done")

async def main():
    print("Starting tasks...")

    # Start other program tasks.
    t1Task = asyncio.create_task(task1())

    # Start the aiorepl task.
    repl = asyncio.create_task(aiorepl.task())

    await asyncio.gather(t1Task, repl)

mainTask = asyncio.run(main())
print("Exited aioREPL")
