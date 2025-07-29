# ✅ Wave To-Do App

A simple, elegant, and printable task tracker built using [H2O Wave](https://wave.h2o.ai/). Designed for productivity and portability — write tasks, mark them complete, and export or print your list with one click.

---

## ✨ Features

- 📝 Add new tasks with ease
- ✅ Check off tasks as complete (with timestamp)
- 🗑 Clear all tasks
- 📄 Export to a `.txt` file for offline access
- 🖨 Print-ready layout with date and task status
- 📱 Mobile-friendly interface

---

## 📦 How to Run

1. **Install H2O Wave**:
   ```bash
   pip install h2o-wave
   ```

2. **Start the Wave server** (in another terminal):
   ```bash
   wave run --no-autoreload todo.py
   ```

3. Open in your browser:
   ```
   http://localhost:10101/todo
   ```

---

## 📂 Folder Structure

```
wave_tutorial/
├── to-do-list/
│   ├── todo.py              # Main Wave app
│   ├── todo-mobile.py       # Mobile-optimized version
│   ├── static/              # Images, exports, etc.
│   └── ...
├── test-grader.xlsx         # Unrelated
└── ...
```

---

## 🚀 Deployment Ideas

- Bundle into a desktop app using PyInstaller or Electron
- Dockerize for easy deployment
- Integrate with Google Tasks or Notion via API (future work)

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).  
You are free to use, share, and modify the software — provided all derivatives remain open-source under the same license.

---

## 🙌 Credits

Built with 💙 using [H2O Wave](https://wave.h2o.ai/).  
By [bdanny2](https://github.com/bdanny2) — CHHS 2025.
