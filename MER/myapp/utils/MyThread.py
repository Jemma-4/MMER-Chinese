import threading
import time

class MyThread(threading.Thread):
    def __init__(self,target, args, name):
        """
        :param target:
        :param args:
        :param name
        """
        threading.Thread.__init__(self, target=target, args=args, name=name)


    def run(self):
        start = time.time()
        print("开始线程：" + self.name)
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
        print("退出线程：" + self.name + " 耗时：" + str(time.time()-start))
