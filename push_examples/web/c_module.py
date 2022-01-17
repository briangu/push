import tornado.web

from push_examples.ex_push_manager import ExamplePushManager
from simple_interpreter import Interpreter, Adder, Multiplier

m = ExamplePushManager()
m.connect()

repl_code_store = m.repl_code_store()

repl_code_store.update({
    "interpreter.Interpreter": Interpreter,
    "interpreter.math.Adder": Adder,
    "interpreter.math.Multiplier": Multiplier
}, sync=True)


# curl -X POST -d'["add", "add", 1, 2, "mul", 3, 4]' -H 'Content-Type: application/json' localhost:11000/math
class MathHandler(tornado.web.RequestHandler):
    def post(self):
        import json
        ops = json.loads(self.request.body.decode("utf-8"))

        # execute via the task manager
        r = local_tasks.apply("interpreter.Interpreter", ops)[0]
        self.write(f"task: {r}")
        self.write("\n")

        # execute via importing directly from the code store
        from repl_code_store.interpreter import Interpreter
        r = Interpreter().apply(ops=ops)[0]
        self.write(f"import: {r}")
        self.write("\n")
        self.finish()


repl_code_store.set("/web/math", MathHandler, sync=True)
