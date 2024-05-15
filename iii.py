import google.generativeai as genai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

GOOGLE_API_KEY="AIzaSyBMunBiGLVEA3tq9saL0F6rEAl4jbyEfsk"
genai.configure(api_key=GOOGLE_API_KEY)

class ChatApp(App):
    def build(self):
        self.model = None
        self.chat = None

        layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView()

        self.output_label = Label(text="Chat output will appear here", size_hint_y=None, height=300)
        self.scroll_view.add_widget(self.output_label)

        self.input_text = TextInput(hint_text="Type your message here")
        self.input_text.bind(on_text_validate=self.send_message)

        self.send_button = Button(text="Send")
        self.send_button.bind(on_press=self.send_message)

        layout.add_widget(self.scroll_view)
        layout.add_widget(self.input_text)
        layout.add_widget(self.send_button)

        return layout

    def start_chat(self):
        generation_config = {
            "candidate_count": 1,
            "temperature": 0.5,
        }

        safety_settings = {
            "HARASSMENT": "BLOCK_NONE",
            "HATE": "BLOCK_NONE",
            "SEXUAL": "BLOCK_NONE",
            "DANGEROUS": "BLOCK_NONE",
        }

        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

        self.chat = self.model.start_chat(history=[])

    def send_message(self, instance):
        if not self.model or not self.chat:
            self.start_chat()

        prompt = self.input_text.text
        self.input_text.text = ""

        response = self.chat.send_message(prompt)

        self.output_label.text += f"\nYou: {prompt}\nAI: {response.text}\n"

        # Atualizar a altura do rótulo para se ajustar ao texto
        self.output_label.height = self.output_label.texture_size[1]

        # Rolagem automática para o final
        self.scroll_view.scroll_y = 0

if __name__ == "__main__":
    ChatApp().run()
