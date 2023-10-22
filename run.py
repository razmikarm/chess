from core import Controller, PromptCLI

ctl = Controller()

prompt = PromptCLI(controller=ctl)
prompt.start()
