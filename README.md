# Online Judge

A minimalist **Django-powered platform** for coding challenges, featuring an **online compiler**, **multi-language support**, and **AI-driven feedback**.

🌐 Live Website: [onlinejudge.ddns.net](http://onlinejudge.ddns.net)  

<p>
  <a href="https://www.loom.com/share/4f91bca40188456ebc052668327e3bbb?sid=28271b34-8abb-4658-b336-604d19dc033e" 
     target="_blank" 
     rel="noopener noreferrer"
     style="display:inline-block; position:relative; text-align:center;">
    <img src="https://drive.google.com/uc?export=view&id=1m-UZQj7GNw_k-I249P8ESRYXtKWu96ta"
         style="width:40%;" 
         alt="Demo Thumbnail"/>
  </a>
</p>

**Tech Stack:**  

![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=flat&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

---

## ✨ Features v1

- 🔐 Authentication (Register & Login)
- 💻 Public Online Compiler (4 languages supported)
- 📚 Solve problems once logged in
- 🤖 AI Review for submitted solutions
- 📜 Submissions history
- 📝 Code Editor with boilerplates, theme-font switcher, etc.

## 🔄 Work in Progress v1

- 🏆 Contests
- 📊 Leaderboard
- ⬆️ Problem Upload Page

---

## 📅 Planned Enhancements v2

- Google Sign-In integration   
- Improved Judge:  
  - Handle both `print` and `return` outputs  
  - Allow multiple correct outputs  
  - Cache results for efficiency  
- Smarter AI Review + IntelliSense in editor  
- Fix indentation, cursor movement, and whitespace handling in editor  
- Remember code snippets per language session  
- Contests & Leaderboard full integration  
- Problem Upload Page completion  
- User Profile Management
---

## Quick Start

```bash
# Clone Repository
git clone https://github.com/PuneethRaavi/AlgoP_OJ.git
cd AlgoP_OJ
# Setup Environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
# Install dependencies-Project Directory
cd OnlineJudge
pip install -r requirements.txt
# Local Environment File
cp .env.example .env
# Prepare Database and Run Server
python manage.py migrate
python manage.py loaddata languages_problems_testdb.json
python manage.py runserver
```
---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
