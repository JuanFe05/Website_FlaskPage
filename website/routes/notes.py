from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models.models import Note
from website import db
import json

notes = Blueprint("notes", __name__)

@notes.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@notes.route("/notes", methods=['GET', 'POST'])
@login_required
def userNotes():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash({'title': "¡Error!", 'message': "¡La nota es demasiado corta!"}, 'error')
            
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash({'title': "¡Genial!", 'message': "¡Nota añadida!"}, 'success')
    
    return render_template("notes.html", user=current_user)

@notes.route('/delete_note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})