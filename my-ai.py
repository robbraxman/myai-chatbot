"""
******************************************************************
MY AI - Author: Rob Braxman
(c) Copyright Braxmobile 2024
License GPL 3.0
******************************************************************
"""

import ollama
import os
import textwrap
import time
import sys
from datetime import datetime
from pathlib import Path

# ==================== CONFIGURATION ====================
MODEL_LIST = [
    'llama3',
    'gemma2',
    'llava',
    'qwen2',
    'phi3:medium',
    'codellama',
    'dolphin-llama3',
]
MULTIMODAL_MODEL = "llava"
BASE_PATH = Path("/home/worker/Documents/vscode-test/")
TEMPERATURE = 0.5

# ==================== ANSI COLOR CODES ====================
BOLD = '\033[1m'
COLORFUL = '\033[92m'
BACK_TO_NORMAL = '\033[0m'


class Config:
    """Manages application configuration and paths."""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.image_path = self.base_path / "images"
        self.log_path = self.base_path / "logs"
        self.text_path = self.base_path / "text"
        self.context_path = self.base_path / "context"
    
    def create_directories(self):
        """Create all required directories if they don't exist."""
        for path in [self.image_path, self.log_path, self.text_path, self.context_path]:
            path.mkdir(parents=True, exist_ok=True)


class AISession:
    """Manages an AI conversation session."""
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.model = ""
        self.system = "You are a helpful AI Assistant."
        self.system_name = "AI Assistant"
        self.context = ""
        self.prompt_count = 0
        self.context_count = 0
        self.first_load = True
    
    def select_model(self):
        """Display menu and select an AI model."""
        while True:
            self._clear_screen()
            print(f"{BOLD}{COLORFUL} WELCOME TO MyAI\n{BACK_TO_NORMAL}{COLORFUL}")
            
            for i, model in enumerate(MODEL_LIST, 1):
                print(f" {i}. Load {model}")
            
            print("\n T. Fine Tune (Session Only)")
            print(" X. Exit\n")
            
            choice = input(f"{COLORFUL} Enter Action ==> {BACK_TO_NORMAL}").strip().lower()
            
            if choice == 't':
                self._configure_system()
                continue
            elif choice == 'x' or choice == '':
                self._exit_app()
            elif choice.isdigit() and 1 <= int(choice) <= len(MODEL_LIST):
                self.model = MODEL_LIST[int(choice) - 1]
                break
            else:
                print(" Invalid selection. Please try again.")
                input(f"{COLORFUL} Press Enter to continue...{BACK_TO_NORMAL}")
    
    def _configure_system(self):
        """Configure system role and instructions."""
        role = input(f"{COLORFUL}\n Who will the AI be (Role)? Blank for Default Assistant? ==> {BACK_TO_NORMAL}").strip()
        
        if role:
            self.system = f"You are {role}. "
            self.system_name = role.title()
        
        additional_instructions = input(f"{COLORFUL} Additional Role Instructions (blank for none) ==> {BACK_TO_NORMAL}").strip()
        self.system += additional_instructions
    
    @staticmethod
    def _clear_screen():
        """Clear the terminal screen."""
        os.system("cls||clear")
    
    @staticmethod
    def _exit_app(message="Bye for now."):
        """Exit the application."""
        print(message)
        sys.exit(0)
    
    def show_help(self):
        """Display help information."""
        help_text = (
            f"{COLORFUL}{BOLD}\n MULTI-LINE ENTRY\n{BACK_TO_NORMAL}{COLORFUL}"
            f"\n 'Ask {self.system_name} a question?'\n"
            f"\n The above prompt allows entry of multiple lines of text."
            f"\n The data will be sent when a blank line is entered."
            f"\n This means you have to hit Enter twice at the end.\n"
            f"{BOLD}\n ADDITIONAL COMMANDS\n{BACK_TO_NORMAL}{COLORFUL}"
            f"\n /i - Upload image (if multimodal model)"
            f"\n /c - Upload context text file"
            f"\n /x - Clear context"
            f"\n /r - Redo current entry"
            f"\n /? - Show this help"
            f"\n /bye - Exit\n{BACK_TO_NORMAL}"
        )
        print(help_text)
        input(f"{COLORFUL}\n Press Enter to continue.{BACK_TO_NORMAL}")
    
    def get_multiline_input(self):
        """Get multiline input from user."""
        lines = []
        while True:
            line = input(" ").strip()
            
            if not line:
                break
            
            line_lower = line.lower()
            
            # Check for special commands
            if line_lower in ['/?', '/bye', '/x', '/c', '/r']:
                lines.append(line)
                break
            
            lines.append(line)
        
        return ' '.join(lines)
    
    def handle_input(self, user_input):
        """Process user input and return action."""
        user_input = user_input.strip()
        
        if user_input.lower() == '/?':
            self.show_help()
            return "help"
        
        if user_input.lower() == '/bye':
            return "exit"
        
        if user_input.lower() == '/x':
            return "clear_context"
        
        if user_input.lower() == '/r':
            return "redo"
        
        if not user_input:
            return "empty"
        
        return "process"
    
    def ask_image(self, text):
        """Check if user wants to upload an image."""
        return '/i' in text.lower()
    
    def ask_context(self, text):
        """Check if user wants to upload context."""
        return '/c' in text.lower()
    
    def get_file_name(self, prompt, path, style=1):
        """Get filename from user."""
        while True:
            filename = input(prompt).strip()
            
            if filename == '/x':
                return ""
            elif filename == '/l':
                return "_last"
            elif filename == '':
                continue
            elif os.path.exists(os.path.join(str(path), filename)):
                return filename
            else:
                print(f" File not found in {path}. Please try again.")
                continue
    
    def format_output(self, text):
        """Format output text for display."""
        lines = text.splitlines()
        wrapped_lines = [textwrap.fill(line, width=80) for line in lines]
        return '\n'.join([' ' * 2 + line for line in wrapped_lines])
    
    def ask_ai(self):
        """Main conversation loop with AI."""
        if self.first_load:
            self._clear_screen()
        
        print(f"{COLORFUL} Ask {self.system_name} a question? (/? Help) {BACK_TO_NORMAL}")
        
        if self.first_load:
            self._show_tips()
            self.first_load = False
        
        # Get user input
        user_input = self.get_multiline_input()
        action = self.handle_input(user_input)
        
        if action == "help":
            return "help"
        elif action == "exit":
            if self.prompt_count > 1 and self._ask_yes_no(f"{COLORFUL}\n Save current context? (y/n) ==> {BACK_TO_NORMAL}"):
                return self._save_checkpoint()
            return "exit"
        elif action == "clear_context":
            self.context = ""
            return "context_cleared"
        elif action == "redo":
            return "redo"
        elif action == "empty":
            if self._ask_yes_no(f"{COLORFUL}\n Exit? (y/n) ==> {BACK_TO_NORMAL}"):
                return "exit"
            return "continue"
        
        # Process normal prompt
        return self._process_prompt(user_input)
    
    def _show_tips(self):
        """Display helpful tips on first load."""
        tips = [
            "-- /c upload a context",
        ]
        if self.model == MULTIMODAL_MODEL:
            tips.append("-- /i upload an image")
        tips.extend([
            "-- /x erase the context",
            "-- /r redo entry",
            "-- /bye to exit",
            f"-- Multiline entry. Hit {BOLD}Enter 2X{BACK_TO_NORMAL}{COLORFUL} to send"
        ])
        
        for tip in tips:
            print(f"{COLORFUL} {tip} {BACK_TO_NORMAL}")
    
    def _ask_yes_no(self, prompt):
        """Ask user a yes/no question."""
        while True:
            response = input(prompt).strip().lower()
            if response in ['y', 'n']:
                return response == 'y'
    
    def _process_prompt(self, prompt):
        """Send prompt to AI and handle response."""
        is_image = self.ask_image(prompt)
        is_context = self.ask_context(prompt)
        
        prompt = prompt.replace('/i', '').replace('/c', '').strip()
        
        image_file = ""
        context_text = ""
        
        # Handle image upload
        if is_image:
            if self.model != MULTIMODAL_MODEL:
                print(f" Model {self.model} is not multimodal. Select a different model.")
                return "error"
            
            input_prompt = (
                f"{COLORFUL}\n UPLOAD AN IMAGE"
                f"\n -- Reading from {self.config.image_path}\n"
                f" -- /x to cancel upload.\n"
                f" -- Enter Filename ==> {BACK_TO_NORMAL}"
            )
            filename = self.get_file_name(input_prompt, str(self.config.image_path))
            
            if filename:
                image_file = str(self.config.image_path / filename)
        
        # Handle context upload
        if is_context:
            input_prompt = (
                f"{COLORFUL}\n UPLOAD A CONTEXT TEXT FILE"
                f"\n -- Reading from {self.config.context_path}"
                f"\n -- Must be a text file."
                f"\n -- /x to cancel upload."
                f"\n -- /l to load last context."
                f"\n -- Enter Filename ==> {BACK_TO_NORMAL}"
            )
            
            filename = self.get_file_name(input_prompt, str(self.config.context_path))
            if not filename:
                return "continue"
            
            try:
                with open(self.config.context_path / filename, 'r') as f:
                    context_text = f.read()
                self.context_count += 1
            except IOError as e:
                print(f" Error reading file: {e}")
                return "error"
        
        # Build prompt with context
        current_date = datetime.now()
        date_context = f"For context, if relevant, current date and time is {current_date.date()} {current_date.time()}. "
        
        full_prompt = f"Context: ''' {context_text} {date_context} ''' Prompt: {prompt}"
        
        print(f"\n {COLORFUL}-- Other commands:  /h help /c context /x clear-context /r redo-entry /bye{BACK_TO_NORMAL}")
        print(f" {COLORFUL}Thinking...Please wait.\n{BACK_TO_NORMAL}")
        
        # Generate response
        try:
            if image_file:
                response = self.client.generate(
                    model=self.model,
                    prompt=full_prompt,
                    context=self.context,
                    system=self.system,
                    images=[image_file]
                )
            else:
                response = self.client.generate(
                    model=self.model,
                    prompt=full_prompt,
                    context=self.context,
                    system=self.system
                )
            
            self.context = response['context']
            formatted = self.format_output(response['response'])
            
            print(f'\n{BOLD}{formatted}{BACK_TO_NORMAL}')
            print(f"{COLORFUL}\n Context Token Count: {len(self.context)}{BACK_TO_NORMAL}")
            
            self._save_query(response['response'], context_text, prompt, image_file)
            self.prompt_count += 1
            
            return "success"
        
        except ollama.ResponseError as e:
            print(f' Error: {e.error}')
            if e.status_code == 404:
                self._exit_app(" Model not found. Please check your model installation.")
            return "error"
    
    def _save_checkpoint(self):
        """Save conversation checkpoint."""
        prompt = "Create a conversation summary in JSONL format. Only include words that are the minimum required to restore context. This will be used to restore the conversation at a later time. Do not add any other commentary."
        # Implementation of checkpoint saving
        return "checkpoint_saved"
    
    def _save_query(self, response, context_text, prompt, image_file):
        """Save query to log file."""
        if not prompt:
            return
        
        timestamp = int(time.time())
        log_file = self.config.log_path / f"query-{timestamp}.log"
        
        log_content = f"Model: {self.model}\n"
        log_content += f"Prompt: {prompt}\n"
        
        if context_text:
            log_content += f"Context: {context_text}\n"
        
        log_content += f"\nResponse: {response}\n"
        
        if image_file:
            log_content += f"\nImage: {image_file}\n"
        
        try:
            log_file.write_text(log_content)
        except IOError as e:
            print(f" Error saving log: {e}")


def main():
    """Main application entry point."""
    config = Config(BASE_PATH)
    config.create_directories()
    
    try:
        client = ollama.Client(host='http://localhost:11434')
    except Exception as e:
        print(f" Error connecting to Ollama: {e}")
        print(" Please ensure Ollama is running on http://localhost:11434")
        sys.exit(1)
    
    session = AISession(client, config)
    session.select_model()
    
    os.system("cls||clear")
    print(f" Starting {session.model} as {session.system_name}\n")
    
    while True:
        try:
            result = session.ask_ai()
            
            if result == "exit":
                break
            elif result == "error":
                continue
            
        except KeyboardInterrupt:
            print(f"\n{COLORFUL} Interrupted by user.{BACK_TO_NORMAL}")
            break
        except Exception as e:
            print(f" Unexpected error: {e}")
    
    os.system("cls||clear")
    print(f' Bye for now. --{session.system_name}\n\n')


if __name__ == "__main__":
    main()
