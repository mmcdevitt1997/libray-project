import sqlite3
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from libraryapp.models import Library
from libraryapp.models import model_factory
from ..connection import Connection



def library_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                l.id,
                l.title,
                l.address
            from libraryapp_library l
            """)

            all_libaries = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                library = Library()
                library.id = row['id']
                library.title = row['title']
                library.address = row['address']

                all_libaries.append(library)

        template = 'libaries/list.html'
        context = {
            'all_libaries': all_libaries
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                title, address
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapp:libaries'))