# solution.py
import threading
import socket
import json
import re
import pygments
from pygments.lexers import PythonLexer, JavaScriptLexer, JavaLexer, CppLexer
from pygments.formatters import HtmlFormatter
from collections import defaultdict

class CodeSync:
    def __init__(self):
        self.notebooks = {}
        self.users = {}
        self.lock = threading.Lock()

    def create_notebook(self, user, notebook_name, is_private):
        with self.lock:
            if notebook_name not in self.notebooks:
                self.notebooks[notebook_name] = {'content': '', 'users': [], 'is_private': is_private}
                self.users[user] = notebook_name
                return True
            else:
                return False

    def edit_notebook(self, user, notebook_name, content):
        with self.lock:
            if notebook_name in self.notebooks:
                self.notebooks[notebook_name]['content'] = content
                self.notebooks[notebook_name]['users'].append(user)
                return True
            else:
                return False

    def get_notebook(self, user, notebook_name):
        with self.lock:
            if notebook_name in self.notebooks:
                return self.notebooks[notebook_name]
            else:
                return None

    def search_notebook(self, user, notebook_name, query):
        with self.lock:
            if notebook_name in self.notebooks:
                content = self.notebooks[notebook_name]['content']
                if re.search(query, content):
                    return True
                else:
                    return False
            else:
                return False

    def syntax_highlight(self, content, language):
        lexer = None
        if language == 'Python':
            lexer = PythonLexer()
        elif language == 'JavaScript':
            lexer = JavaScriptLexer()
        elif language == 'Java':
            lexer = JavaLexer()
        elif language == 'C++':
            lexer = CppLexer()
        if lexer:
            formatter = HtmlFormatter()
            highlighted_content = pygments.highlight(content, lexer, formatter)
            return highlighted_content
        else:
            return content

    def code_completion(self, content, language):
        # This is a simple implementation of code completion, you may want to use a more advanced library or service
        if language == 'Python':
            return ['print()', 'len()', 'range()']
        elif language == 'JavaScript':
            return ['console.log()', 'document.getElementById()', 'window.alert()']
        elif language == 'Java':
            return ['System.out.println()', 'String.length()', 'for (int i = 0; i < 10; i++)']
        elif language == 'C++':
            return ['std::cout <<', 'std::string str;', 'for (int i = 0; i < 10; i++)']
        else:
            return []

    def version_control(self, user, notebook_name, version):
        with self.lock:
            if notebook_name in self.notebooks:
                if version in self.notebooks[notebook_name]['versions']:
                    return self.notebooks[notebooks_name]['versions'][version]
                else:
                    return None
            else:
                return None

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            data = json.loads(data.decode('utf-8'))
            if data['action'] == 'create_notebook':
                self.create_notebook(data['user'], data['notebook_name'], data['is_private'])
                client_socket.send(json.dumps({'result': 'notebook created'}).encode('utf-8'))
            elif data['action'] == 'edit_notebook':
                self.edit_notebook(data['user'], data['notebook_name'], data['content'])
                client_socket.send(json.dumps({'result': 'notebook edited'}).encode('utf-8'))
            elif data['action'] == 'get_notebook':
                notebook = self.get_notebook(data['user'], data['notebook_name'])
                if notebook:
                    client_socket.send(json.dumps({'result': notebook}).encode('utf-8'))
                else:
                    client_socket.send(json.dumps({'result': 'notebook not found'}).encode('utf-8'))
            elif data['action'] == 'search_notebook':
                result = self.search_notebook(data['user'], data['notebook_name'], data['query'])
                if result:
                    client_socket.send(json.dumps({'result': 'search result found'}).encode('utf-8'))
                else:
                    client_socket.send(json.dumps({'result': 'search result not found'}).encode('utf-8'))
            elif data['action'] == 'syntax_highlight':
                highlighted_content = self.syntax_highlight(data['content'], data['language'])
                client_socket.send(json.dumps({'result': highlighted_content}).encode('utf-8'))
            elif data['action'] == 'code_completion':
                completion = self.code_completion(data['content'], data['language'])
                client_socket.send(json.dumps({'result': completion}).encode('utf-8'))
            elif data['action'] == 'version_control':
                version = self.version_control(data['user'], data['notebook_name'], data['version'])
                if version:
                    client_socket.send(json.dumps({'result': version}).encode('utf-8'))
                else:
                    client_socket.send(json.dumps({'result': 'version not found'}).encode('utf-8'))
            else:
                client_socket.send(json.dumps({'result': 'unknown action'}).encode('utf-8'))

        client_socket.close()

    def start_server(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f'Server listening on {host}:{port}')

        while True:
            client_socket, address = server_socket.accept()
            print(f'Connected to {address}')
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    codesync = CodeSync()
    codesync.start_server('localhost', 12345)