import streamlit as st
import streamlit.components.v1 as components
import json

def render_audio_speaker(text_to_speak: str = "", auto_speak: bool = True):
    """
    Clean Text-To-Speech Audio Speaker Component using Web Speech API.
    Auto-speaks the question or evaluation feedback once per question/state change.
    Guards against duplicate speech playback during session state reruns.
    """
    if not auto_speak or not text_to_speak.strip():
        return None

    # Do not re-trigger speech if the exact same text was already spoken for this question state
    if st.session_state.get("_last_spoken_text") == text_to_speak.strip():
        return None

    st.session_state["_last_spoken_text"] = text_to_speak.strip()
    safe_text = json.dumps(text_to_speak)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="background: transparent; margin: 0; padding: 0; overflow: hidden;">
        <script>
            (function() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const text = {safe_text};
                    if (text && text.trim().length > 0) {{
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.rate = 1.0;
                        utterance.pitch = 1.0;
                        utterance.lang = 'en-US';
                        window.speechSynthesis.speak(utterance);
                    }}
                }}
            }})();
        </script>
    </body>
    </html>
    """
    return components.html(html_code, height=0, width=0)
