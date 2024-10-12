from bitmap import (BADAPPLE_WIDTH as width,
                    BADAPPLE_HEIGHT as height,
                    BADAPPLE_FRAMES as frames,
                    BADAPPLE_LIST as badapple)

import random
import os,sys
from time import sleep,perf_counter as time
import winsound
import asyncio
from asyncio import sleep as asyncSleep
from datetime import timedelta
from typing import Generator

# density = '■ '
density = ' @'
frame_rate = 1./30.

# hex_dict = {'0': '0000',
#             '1': '0001',
#             '2': '0010',
#             '3': '0011',
#             '4': '0100',
#             '5': '0101',
#             '6': '0110',
#             '7': '0111',
#             '8': '1000',
#             '9': '1001',
#             'a': '1010',
#             'b': '1011',
#             'c': '1100',
#             'd': '1101',
#             'e': '1110',
#             'f': '1111'}

def ListHorizonal(intList:list) -> Generator[int,None,list[int]]:
    num = int()
    for i in intList:
        # int sang binary
        binStr = f"{i:8b}"
        for j in binStr:
            num = 0
            if j == '1':
                num = 1
            yield num

def Load() -> Generator[str,None,list[str]]:
    chunk = []
    count = len(badapple)
    size = int(46)
    for i,item in enumerate(badapple):
        outp = str()
        x = int(size*i/(count-1))
        for j in ListHorizonal(item):
            chunk.append(density[j])
            if len(chunk) == width:
                outp += f" {''.join(map(str,chunk))}\n"
                chunk = []
        print(f"Loading: |{u'█'*x}{(' '*(size-x))}| {(i/count)*100:3.0f}%",flush=True,end='\r',file=sys.stdout)
        yield outp
    print('\nDone',flush=True,end='\r',file=sys.stdout)
    sleep(3)

async def PlaySoundWav() -> None:
    await asyncSleep(frame_rate)
    winsound.PlaySound(f"{os.path.split(os.path.abspath(sys.argv[0]))[0]}\\bad-apple-audio.wav",winsound.SND_ASYNC)

async def PlayBadApple() -> None:
    frame_list = list(Load())
    wh = width * height
    wspace = int(len(frame_list[0]) / wh * width / 2 - 25)
    time_start = current_time = target_time = time()
    rand = prev_f = fps = sleep = sleep_time = timeTotal = float()
    outp = str()
    for index in range(frames - 1):
        prev_f,current_time = current_time, time()
        outp = frame_list[index]
        timeTotal = current_time - time_start
        rand = random.uniform(0.,frame_rate/2.)
        target_time += frame_rate
        await asyncSleep(rand)
        sleep_time = target_time - time()
        sleep = sleep_time + rand
        # if current_time != prev_f:
        fps = 1. / (current_time - prev_f)
        if sleep_time > 0.:
            await asyncSleep(sleep_time)
        sys.stdout.write(f"\r\033[99A\033[2K|{'=' * wspace}|Frame: {(index + 1):4} fps: {(fps):4.1f} Sleep: {(sleep * 1000):4.1f}ms Time: {str(timedelta(seconds=timeTotal)).split('.')[0].split(':',maxsplit=1)[1]}|{'=' * wspace}|\n{outp}\n\r")
        sys.stdout.flush()
    input('')
    exit()

async def main() -> None:
    await asyncio.gather(PlaySoundWav(),PlayBadApple())

if __name__ == '__main__':
    asyncio.run(main())
