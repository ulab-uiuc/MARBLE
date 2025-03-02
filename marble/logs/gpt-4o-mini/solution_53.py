# solution.py

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image, ImageEnhance
import io
import base64
import json

# Initialize Flask application and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Store the current state of the photo and its history
photo_state = None
photo_history = []
comments = []

# Function to convert image to base64 for rendering in HTML
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Route to render the main editing page
@app.route('/')
def index():
    return render_template('index.html', photo=photo_state)

# SocketIO event to handle real-time edits
@socketio.on('edit_photo')
def handle_edit(data):
    global photo_state
    # Update the photo state based on user edits
    photo_state = Image.open(io.BytesIO(base64.b64decode(data['photo'])))
    # Save the current state to history
    photo_history.append(image_to_base64(photo_state))
    # Emit the updated photo to all connected clients
    emit('update_photo', {'photo': image_to_base64(photo_state)}, broadcast=True)

# SocketIO event to handle comments
@socketio.on('add_comment')
def handle_comment(data):comments.append({'comment': data['comment'], 'edit_id': data['edit_id'], 'timestamp': data['timestamp']})    # Emit the new comment to all connected clients
    emit('new_comment', {'comment': data['comment']}, broadcast=True)
    # Emit the current comments to all connected clients
    emit('current_comments', {'comments': comments}, broadcast=True)

# SocketIO event to handle version control
@socketio.on('revert_photo')
def handle_revert(data):
    global photo_state
    # Revert to the specified version
    if 0 <= data['version'] < len(photo_history):
        photo_state = Image.open(io.BytesIO(base64.b64decode(photo_history[data['version']])))
        emit('update_photo', {'photo': image_to_base64(photo_state)}, broadcast=True)

# Function to adjust brightness
def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Function to adjust contrast
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# Main function to run the application
if __name__ == '__main__':
    # Load an initial photo
    initial_image = Image.new('RGB', (800, 600), color='white')
    photo_state = initial_image
    photo_history.append(image_to_base64(photo_state))
    socketio.run(app, debug=True)

# HTML and JavaScript for the front-end (index.html)
# This part would typically be in a separate HTML file, but included here for completeness.
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhotoCollabEditor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
</head>
<body>
    <h1>PhotoCollabEditor</h1>
    <img id="photo" src="data:image/png;base64,{{ photo }}" alt="Collaborative Photo" />
    <input type="file" id="upload" />
    <button onclick="adjustBrightness(1.2)">Increase Brightness</button>
    <button onclick="adjustContrast(1.2)">Increase Contrast</button>
    <div id="comments"></div>
    <input type="text" id="commentInput" placeholder="Leave a comment..." />

    <button onclick="addComment()">Submit Comment</button>
    <input type="hidden" id="editId" value="some_edit_id" />
    <script>
        const socket = io();

        // Function to handle photo upload
        document.getElementById('upload').onchange = function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.src = e.target.result;
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    const dataURL = canvas.toDataURL('image/png');
                    socket.emit('edit_photo', { photo: dataURL.split(',')[1] });
                }
    // Function to reply to a specific comment
    const replyButton = document.createElement('button');
    replyButton.innerText = 'Reply';
    replyButton.onclick = function() {
        const reply = prompt('Reply to comment: ' + comment);
        if (reply) {
            socket.emit('add_comment', { comment: reply });
        }
    };
    document.getElementById('replySection').appendChild(replyButton);;
            };
            reader.readAsDataURL(file);
        };

        // Function to adjust brightness
        function adjustBrightness(factor) {
            socket.emit('edit_photo', { photo: document.getElementById('photo').src.split(',')[1] });
        }

        // Function to adjust contrast
        function adjustContrast(factor) {
            socket.emit('edit_photo', { photo: document.getElementById('photo').src.split(',')[1] });
        }

        // Function to add a comment
        function addComment() {
            const comment = document.getElementById('commentInput').value;
            socket.emit('add_comment', { comment: comment });
            document.getElementById('commentInput').value = '';
        }

        // Listen for updated photo from server
        socket.on('update_photo', function(data) {
            document.getElementById('photo').src = 'data:image/png;base64,' + data.photo;
        });

        // Listen for new comments
        socket.on('new_comment', function(data) {
            const commentsDiv = document.getElementById('comments');
            commentsDiv.innerHTML += '<p>' + data.comment + '</p>';
        });
        // Listen for current comments
        socket.on('current_comments', function(data) {
            data.comments.forEach(function(comment) {
                commentsDiv.innerHTML += '<p>' + comment + '</p>';
            });
        });
    </script>
</body>
</html>
"""
# Save the HTML content to a file
with open('templates/index.html', 'w') as f:
    f.write(html_content)