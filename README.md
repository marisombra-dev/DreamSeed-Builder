
---

````markdown
# 🌱 DreamSeed Builder

**A beautifully structured product vision doc, crafted from your idea in minutes.**  
Use it to brief any LLM, developer, co-founder, or investor — and move from spark 💡 to strategy 🚀 faster than ever.

---

## ✨ What is DreamSeed?

DreamSeed turns vague inspiration into a clear, actionable concept brief.  
You give it an idea, audience, and tone — it returns a well-organized document ready to be developed, marketed, or pitched.

We position ourselves **between the idea and the execution**.  
DreamSeed is the bridge.

---

## 🎁 Features

- 🔍 Side-panel input for easy idea capture  
- 🧠 LLM-powered outline & vision generation (locally or via API)  
- 📄 Export in Markdown, PDF, or TXT  
- 🪄 Optional deep-dive prompt engineering built in  
- 🐋 Supports local Ollama or OpenAI API  
- 💻 Easy setup, no prior experience required  

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/pattipur/DreamSeed-Builder.git
cd DreamSeed-Builder
````

### 2. Install dependencies

We recommend using a virtual environment:

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
streamlit run app.py
```

💡 For **local generation**, install [Ollama](https://ollama.com) and make sure it’s running on:

```
http://localhost:11434
```

---

## 🐳 Optional: Run with Docker

If you'd rather use Docker:

```bash
docker-compose up --build
```

---

## 🛠️ Tech Stack

* `Streamlit` for UI
* `FPDF` for PDF export
* `Ollama` or `OpenAI` for generation
* `Python` 3.10+
* `Docker` (optional)

---

## 📂 File Structure

```
dreamseed-builder/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .streamlit/
│   └── config.toml
├── outputs/
│   ├── (your generated files will appear here)
```

---

## 🧠 Why DreamSeed?

Because ideas deserve better than a napkin scribble or lost Notion tab.
Because the first step is often the hardest.
Because you don’t need another brainstorm — you need **a blueprint**.

---

## 🪪 License

[MIT License](LICENSE)

---

🧠 Author

Created by Marisombra — the shadow tide.

A developer, game designer, and bilingual dreamer.

Check out more projects at https://github.com/pattipur


