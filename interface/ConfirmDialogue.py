from rich.prompt import Confirm

def confirmDialogue(msg: str) -> bool:
    return Confirm.ask(msg)
