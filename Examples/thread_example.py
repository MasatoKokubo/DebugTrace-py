# thread_example.py
import threading
import time
import debugtrace # TODO: Remove after debugging

def aThread(index: int):
    _ = debugtrace.enter() # TODO: Remove after debugging
    debugtrace.print('index', index)
    debugtrace.print('ident', threading.get_ident())
#   debugtrace.print('native_id', threading.get_native_id())
    debugtrace.print('before sleep')
    time.sleep(1)
    debugtrace.print('after sleep')
    
def main():
    _ = debugtrace.enter() # TODO: Remove after debugging
    threadCount = 4
    threads = []
    for index in range(threadCount):
        threads.append(threading.Thread(target=aThread, name="a Thread", args=(index,)))
        threads[index].start()
        time.sleep(0.1)

    for index in range(threadCount):
        threads[index].join()

main()
