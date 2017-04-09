import queue
import threading
class Task:
    def __init__(self,id,func):
        self.id = id
        self.func = func

    def run(self):
        self.func()

class TaskQueue:
    def __init__(self):
        self.tasks = queue.Queue()
        pass

    def add_task(self,task):
        self.tasks.put(task)
        pass
    def cancel_task_by_id(self,id):
        pass
    def cancel_task(self,task):
        pass

    def pop_task(self):
        task = None
        try:
            task = self.tasks.get(block=True,timeout=0.1)
        except queue.Empty:
            pass
        return task

    def run_task(self,maxlimit = 0):
        if self.tasks.empty() : return
        if maxlimit <= 0:
            while not self.tasks.empty():
                task = self.tasks.get()
                task.run()
        else:
            index = 0
            while not self.tasks.empty():
                task = self.tasks.get()
                task.run()
                index = index + 1
                if index >= maxlimit :
                    return


class TaskManager:

    class _ThreadWrapper:
        def __init__(self,taskqueue):
            self.stop = False
            self.taskqueue = taskqueue

            pass
        def stop(self):
            self.stop = True
        def run(self):
            while not self.stop:
                task = self.taskqueue.pop_task()

                if task is not None:
                    task.run()




    def __init__(self,threadcount = 3):
        self.main_queue = TaskQueue()
        self.async_queues = TaskQueue()
        self.name_async_queues = {}
        self.taskcount = 0
        self.threadwrappers = []
        self.set_thread_num(threadcount)
        pass


    def newid(self):
        self.taskcount += 1
        return self.taskcount

    def set_thread_num(self,num):
        """
        Set the thread num to the task manager. when num > current thread num , create new threads
        when num < current thread num, stop some threads and remove
        :param num:
        :return:
        """
        nownum = len(self.threadwrappers)
        if nownum == num : return
        if nownum > num:
            for wrapper in self.threadwrappers[num :nownum]:
                wrapper.stop()
            del self.threadwrappers[num:nownum]
        else:
            for i in range(nownum,num):
                wrapper = TaskManager._ThreadWrapper(self.async_queues)

                thread = threading.Thread(None,wrapper.run)
                thread.setDaemon(True)
                thread.start()

                self.threadwrappers.append(wrapper)



    def add_async_task(self,func):
        newtask = Task(self.newid(),func)
        self.async_queues.add_task(newtask)

    def create_async_queue(self,name):
        taskqueue = TaskQueue()
        wrapper = TaskManager._ThreadWrapper(taskqueue)
        thread = threading.Thread(None,wrapper.run,name)
        thread.setDaemon(True)
        thread.start()
        self.name_async_queues[name] = wrapper

    def add_main_task(self,func):
        newtask = Task(self.newid(), func)
        self.main_queue.add_task(newtask)
    def add_name_task(self,name,func):
        newtask = Task(self.newid(), func)
        self.name_async_queues[name].taskqueue.add_task(newtask)

    def run_main_tasks(self,maxlimit):

        self.main_queue.run_task(maxlimit)

    def run_threads(self):
        pass
