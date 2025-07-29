"""Wave To-Do List App"""

from typing import List
from h2o_wave import Q, app, ui
from datetime import datetime
import base64

TASK_ID = 0


class TodoItem:
    """A simple class that represents a to-do item."""
    def __init__(self, text):
        global TASK_ID
        TASK_ID += 1
        self.id = f'todo_{TASK_ID}'
        self.text = text
        self.done = False
        self.done_at = None  # ✅ Timestamp when marked done


@app('/todo', mode='multicast')
async def serve(q: Q):
    """Main entry point: handles all UI actions."""
    if q.args.new_todo:
        new_todo(q)
    elif q.args.add_todo:
        add_todo(q)
    elif q.args.clear_todos:
        clear_todos(q)
    elif q.args.export_todos:
        export_todos(q)
    elif q.args.print_view:
        show_print_view(q)
    else:
        show_todos(q)
    await q.page.save()


def show_todos(q: Q):
    """Render the to-do list and optional export/print buttons."""
    todos: List[TodoItem] = q.user.todos

    if todos is None:
        q.user.todos = todos = [
            TodoItem('Do this'),
            TodoItem('Do that'),
            TodoItem('Do something else'),
        ]

    for todo in todos:
        if todo.id in q.args:
            if q.args[todo.id] and not todo.done:
                todo.done = True
                todo.done_at = datetime.now()
            elif not q.args[todo.id] and todo.done:
                todo.done = False
                todo.done_at = None

    done = [ui.checkbox(name=todo.id, label=todo.text, value=True, trigger=True)
            for todo in todos if todo.done]
    not_done = [ui.checkbox(name=todo.id, label=todo.text, trigger=True)
                for todo in todos if not todo.done]

    q.page['form'] = ui.form_card(box='1 1 4 10', items=[
        ui.text_l('To Do'),
        ui.buttons([
            ui.button(name='new_todo', label='New To Do...', primary=True),
            ui.button(name='clear_todos', label='Clear All', icon='Delete'),
            ui.button(name='export_todos', label='Export to TXT', icon='Download'),
            ui.button(name='print_view', label='Print View', icon='Print'),
        ]),
        *not_done,
        *([ui.separator('Done')] if done else []),
        *done,
    ])

    if hasattr(q.client, 'exported_text'):
        q.page['download'] = ui.markup_card(
            box='1 11 3 2',
            title='Export Ready',
            content=make_download_link(q.client.exported_text)
        )
    else:
        try:
            del q.page['download']
        except KeyError:
            pass


def add_todo(q: Q):
    """Add a new to-do item to the list."""
    q.user.todos.insert(0, TodoItem(q.args.text or 'Untitled'))
    show_todos(q)


def new_todo(q: Q):
    """Show form to enter a new to-do item."""
    q.page['form'] = ui.form_card(box='1 1 3 10', items=[
        ui.text_l('New To Do'),
        ui.textbox(name='text', label='What needs to be done?', multiline=True),
        ui.buttons([
            ui.button(name='show_todos', label='🔙 Back to Tasks'),
            ui.button(name='add_todo', label='Add', primary=True),
        ]),
    ])


def clear_todos(q: Q):
    """Clear all to-do items and remove export text."""
    q.user.todos = []
    try:
        delattr(q.client, 'exported_text')
    except (AttributeError, KeyError):
        pass
    show_todos(q)


def export_todos(q: Q):
    """Convert the to-do list to plain text for export."""
    todos: List[TodoItem] = q.user.todos or []
    lines = ['To-Do List\n', '===========\n\n']
    for todo in todos:
        status = '[x]' if todo.done else '[ ]'
        lines.append(f'{status} {todo.text}\n')

    q.client.exported_text = ''.join(lines)
    show_todos(q)


def make_download_link(text: str) -> str:
    """Create a base64-encoded download link from text."""
    text = text or 'No content to export.'
    encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return f'''
    <a download="todo_export.txt" href="data:text/plain;base64,{encoded}" 
       style="font-size:18px; display:inline-block; margin-top:12px;">
       📄 Click here to download your To-Do List
    </a>
    '''


def show_print_view(q: Q):
    """Render a clean, printable view of the to-do list with timestamps."""
    todos: List[TodoItem] = q.user.todos or []
    now = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')

    not_done = [f'<li>⬜ {todo.text}</li>' for todo in todos if not todo.done]

    done = [
        f'<li>✅ {todo.text} '
        f'<span style="font-size:12px; color:gray;">({todo.done_at.strftime("%b %d, %Y %I:%M %p")})</span></li>'
        for todo in todos if todo.done and todo.done_at
    ]

    html_lines = [
        f'<h2>📋 To-Do List</h2>',
        f'<p><strong>Date:</strong> {now}</p>',
        '<hr>',
        '<h3>⬜ Tasks To Do</h3>',
        '<ul style="font-size:18px;">'
    ] + (not_done if not_done else ['<li><em>None</em></li>']) + [
        '</ul>',
        '<h3>✅ Completed Tasks</h3>',
        '<ul style="font-size:18px; color:gray;">'
    ] + (done if done else ['<li><em>None</em></li>']) + [
        '</ul>',
        '<hr>',
        '<p style="font-size:12px; color:gray;">Generated by your To-Do App</p>',
        '<script>setTimeout(() => window.print(), 300);</script>'
    ]

    q.page['print'] = ui.markup_card(
        box='1 1 6 10',
        title='Printable To-Do List',
        content='\n'.join(html_lines)
    )
