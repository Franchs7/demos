"""
使用协程的概念，达到以下目的， 输入a，b，c，d四个整数，打印(a+b)*(c+d)的值
"""
import asyncio, os
from threading import current_thread



async def sum(a, b):
    print("【%s-%s】coroutine start to do: %s + %s" % (os.getpid(), current_thread().getName(), a, b))
    await asyncio.sleep(1) # 模拟耗时1秒的IO操作，自动切换协程
    r = int(a) + int(b)
    print("【%s-%s】coroutine end for : %s + %s,  result is %s" % (os.getpid(), current_thread().getName(), a, b, r))
    return r



def main(a, b, c, d):
    loop = asyncio.get_event_loop()
    task = asyncio.gather(
        sum(a, b),
        sum(c, d)
    )
    loop.run_until_complete(task)
    r1, r2 = task.result()
    r = r1 * r2
    print("【%s-%s】%s * %s = %s" % (os.getpid(), current_thread().getName(), r1, r2, r))
    loop.close()

if __name__ == '__main__':
    main(1, 2, 3, 4)