#!../../venv/bin/python3
from push_examples.ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

dt = m.local_tasks()
r = dt.apply(src=lambda *args, **kwargs: repl_ts.flatten())
print(r)
