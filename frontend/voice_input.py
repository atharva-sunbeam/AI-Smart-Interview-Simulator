import streamlit as st
import streamlit.components.v1 as components

def render_voice_input_widget(key: str = "voice_input"):
    """
    Lightweight, bi-directional Web Speech Recognition component.
    Transcribes spoken audio into the parent Streamlit <textarea> DOM element in real-time
    using window.parent synthetic events without blocking DOM rendering or causing lag.
    """
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
            
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Inter', sans-serif;
                background: transparent;
                padding: 2px 0;
                display: flex;
                align-items: center;
                gap: 12px;
                color: #e2e8f0;
                overflow: hidden;
            }
            
            .voice-btn {
                background: linear-gradient(135deg, rgba(79, 70, 229, 0.35), rgba(6, 182, 212, 0.35));
                border: 1px solid rgba(79, 70, 229, 0.6);
                color: #38bdf8;
                padding: 7px 15px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.2s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            }
            
            .voice-btn:hover {
                background: linear-gradient(135deg, rgba(79, 70, 229, 0.55), rgba(6, 182, 212, 0.55));
                border-color: #38bdf8;
                box-shadow: 0 0 14px rgba(56, 189, 248, 0.4);
                transform: translateY(-1px);
            }
            
            .voice-btn.recording {
                background: rgba(239, 68, 68, 0.35);
                border-color: #ef4444;
                color: #f87171;
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6); }
                70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
                100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
            }
            
            .status-msg {
                font-size: 12px;
                color: #94a3b8;
                font-weight: 500;
            }
        </style>
    </head>
    <body>
        <button class="voice-btn" id="btnMicRec" onclick="toggleRec()">
            <span id="micIcon">🎤</span> <span id="btnLabel">Record Voice Answer</span>
        </button>
        <span class="status-msg" id="statusText">Click to speak your answer — speech will transcribe into the box below</span>

        <script>
            let recognition = null;
            let isRecording = false;
            let finalTranscript = '';

            function injectTextIntoParentTextarea(text) {
                if (!text || !text.trim()) return;
                try {
                    const parentWin = window.parent;
                    const parentDoc = parentWin.document;
                    const textareas = parentDoc.querySelectorAll('textarea');
                    if (textareas && textareas.length > 0) {
                        const target = textareas[textareas.length - 1];

                        const nativeSetter = Object.getOwnPropertyDescriptor(
                            parentWin.HTMLTextAreaElement.prototype,
                            "value"
                        ).set;

                        if (target._reactValueTracker) {
                            target._reactValueTracker.setValue(Math.random().toString());
                        }

                        nativeSetter.call(target, text);

                        target.dispatchEvent(new parentWin.Event('input', { bubbles: true }));
                        target.dispatchEvent(new parentWin.Event('change', { bubbles: true }));
                    }
                } catch (err) {
                    console.error("Parent DOM injection error:", err);
                }
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';

                recognition.onstart = () => {
                    isRecording = true;
                    document.getElementById('btnMicRec').classList.add('recording');
                    document.getElementById('btnLabel').innerText = 'Stop & Insert Answer';
                    document.getElementById('micIcon').innerText = '🔴';
                    document.getElementById('statusText').innerText = 'Listening... Speak clearly into your microphone';
                };

                recognition.onresult = (event) => {
                    let interim = '';
                    for (let i = event.resultIndex; i < event.results.length; ++i) {
                        if (event.results[i].isFinal) {
                            finalTranscript += event.results[i][0].transcript + ' ';
                        } else {
                            interim += event.results[i][0].transcript;
                        }
                    }

                    const fullText = (finalTranscript + ' ' + interim).trim();
                    if (fullText) {
                        document.getElementById('statusText').innerText = '🗣️ Transcribing: "' + fullText.substring(0, 45) + '..."';
                        injectTextIntoParentTextarea(fullText);
                    }
                };

                recognition.onend = () => {
                    isRecording = false;
                    document.getElementById('btnMicRec').classList.remove('recording');
                    document.getElementById('btnLabel').innerText = 'Record Voice Answer';
                    document.getElementById('micIcon').innerText = '🎤';
                    const fullText = finalTranscript.trim();
                    if (fullText) {
                        document.getElementById('statusText').innerText = '✅ Transcribed answer inserted automatically!';
                        injectTextIntoParentTextarea(fullText);
                    } else {
                        document.getElementById('statusText').innerText = 'Ready. Click to speak your answer.';
                    }
                };

                recognition.onerror = (event) => {
                    document.getElementById('statusText').innerText = 'Mic error: ' + event.error;
                    isRecording = false;
                    document.getElementById('btnMicRec').classList.remove('recording');
                    document.getElementById('btnLabel').innerText = 'Record Voice Answer';
                    document.getElementById('micIcon').innerText = '🎤';
                };
            } else {
                document.getElementById('statusText').innerText = 'Web Speech Recognition not supported in this browser (Use Chrome or Edge).';
            }

            function toggleRec() {
                if (!recognition) return;
                if (isRecording) {
                    recognition.stop();
                } else {
                    finalTranscript = '';
                    try {
                        recognition.start();
                    } catch (err) {
                        console.error(err);
                    }
                }
            }
        </script>
    </body>
    </html>
    """
    return components.html(html_code, height=45)
