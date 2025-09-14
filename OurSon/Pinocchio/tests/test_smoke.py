from nestor.dialogue.manager import DialogueManager

def test_respond_smoke():
    dm = DialogueManager()
    out = dm.respond("Hello")
    assert isinstance(out, str)
