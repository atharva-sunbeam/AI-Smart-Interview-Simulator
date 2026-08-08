from frontend.audio_speaker import render_audio_speaker

def render_interviewer_avatar(text_to_speak="", expression="welcoming", persona="Alex", auto_speak=True, height=420):
    """
    Deprecated avatar component replaced by clean Text-to-Speech audio speaker.
    """
    return render_audio_speaker(text_to_speak=text_to_speak, auto_speak=auto_speak)
