import sched
import time
import datetime
import threading
import subprocess
import os
import sys
import importlib.util
from .debug import discord_screenshot
from zrcl3_uses import file

class Scheduler:
    DEFER_DAY : bool = False
    config : dict = file.FileProperty('config.toml')

    def __init__(self, folder_path, overwrite_current_time=None):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.folder_path = folder_path
        self.overwrite_current_time = overwrite_current_time if overwrite_current_time else datetime.datetime.now()
        self.tasks = [f for f in os.listdir(folder_path) if f.endswith('.py')]
        print(f"Scheduler initialized with current time set to {self.overwrite_current_time}")
        self.load_and_schedule_tasks()
        # set every 5 min
        self.scheduler.enter(300, 1, discord_screenshot)


    def load_and_schedule_tasks(self):
        for task in self.tasks:
            if self.config.get(task, True) is False:
                print(f"Skipping task {task} as it is marked as OFF")
                continue

            module = self.load_task_module(task)
            if not module:
                continue
            if hasattr(module, 'OFF'):
                print(f"Skipping task {task} as it is marked as OFF")
                continue
            
            if hasattr(module, 'RUNTIME') and hasattr(module, 'MAXRUNTIME'):
                print(f"Module {task} loaded successfully")
                print(f"Task {task} loaded with RUNTIME {module.RUNTIME} and MAXRUNTIME {module.MAXRUNTIME/60} minutes")
                self.schedule_task(module.RUNTIME, module.MAXRUNTIME, task)

    def schedule_task(self, run_time, max_runtime, task):
        run_time = datetime.datetime.strptime(run_time, "%I%M %p").time()
        scheduled_time = datetime.datetime.combine(self.overwrite_current_time.date(), run_time)
        if scheduled_time < self.overwrite_current_time:
            if self.DEFER_DAY:
                scheduled_time += datetime.timedelta(days=1)
            else:
                return
        delay = (scheduled_time - self.overwrite_current_time).total_seconds()
        print(f"Scheduling {task} to run at {scheduled_time} which is in {delay} seconds")
        self.scheduler.enter(delay, 1, self.execute_task, (int(max_runtime), task))

    def execute_task(self, max_runtime, task):
        print(f"Executing task {task} with a maximum runtime of {max_runtime} seconds")
        thread = threading.Thread(target=self.run_task, args=(task, max_runtime))
        thread.start()

    def run_task(self, task, max_runtime):
        task_module = self.load_task_module(task)
        if task_module:
            print(f"Starting prerun for {task}")
            if hasattr(task_module, 'prerun'):
                task_module.prerun()
            print(f"Starting main run for {task}")
            process = subprocess.Popen(['python', os.path.join(self.folder_path, task)])
            timer = threading.Timer(max_runtime, self.stop_task, [task_module, process])
            timer.start()
            process.wait()
            timer.cancel()
            process.poll() 
            if hasattr(task_module, 'postrun'):
                task_module.postrun()

    def load_task_module(self, task):
        task_path = os.path.join(self.folder_path, task)
        spec = importlib.util.spec_from_file_location(task, task_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[task] = module
        spec.loader.exec_module(module)
        
        return module

    def stop_task(self, task_module, process):
        print(f"Stopping task {task_module.__name__} due to exceeding maximum runtime")
        if hasattr(task_module, 'stop'):
            task_module.stop(process)  # Ensure the module has a stop method to call for clean shutdown
        process.terminate()
        print("Task was forcefully terminated.")

    def has_tasks(self):
        return len(self.scheduler.queue) > 1
