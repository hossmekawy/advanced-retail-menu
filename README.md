# 🍽️ Advanced Digital Restaurant Menu

A modern, multilingual digital restaurant menu application built with Flask, featuring Arabic and English support with a responsive design.

## ✨ Features

- 🌐 **Multilingual Support**: Full Arabic and English localization
- 📱 **Responsive Design**: Mobile-first approach with Tailwind CSS
- 🔐 **Admin Panel**: Complete menu management system
- 🖼️ **Image Upload**: Base64 encoding for easy deployment
- 📁 **Category Management**: Hierarchical category and subcategory organization
- 🛍️ **Product Management**: Full CRUD operations for menu items
- 🎨 **Customizable Themes**: Brand colors and logo customization
- 🔍 **Search Functionality**: Real-time product search
- 📊 **Dashboard**: Admin statistics and quick actions
- 🔒 **User Authentication**: Secure admin access

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hossmekawy/advanced-retail-menu.git
   cd advanced-retail-menu
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Main menu: http://localhost:5000
   - Admin panel: http://localhost:5000/admin
   - Default admin credentials: `admin` / `admin123`

## 📖 Usage

### For Restaurant Owners

1. **Login to Admin Panel**: Navigate to `/admin` and login
2. **Configure Settings**: Set your restaurant name, logo, and brand colors
3. **Create Categories**: Organize your menu with main categories
4. **Add Subcategories**: Create subcategories for better organization
5. **Add Products**: Upload product images, set prices, and descriptions
6. **Customize Appearance**: Match your brand colors and style

### For Customers

1. **Browse Menu**: View organized categories and products
2. **Search Products**: Use the search bar to find specific items
3. **View Details**: Click on products to see detailed information
4. **Language Toggle**: Switch between Arabic and English

## 🏗️ Project Structure

```
advanced-retail-menu/
├── app/
│   ├── __init__.py
│   ├── models.py              # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py          # Admin panel routes
│   │   ├── api.py            # API endpoints
│   │   └── core.py           # Main application routes
│   ├── templates/
│   │   ├── admin/            # Admin panel templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Homepage
│   │   └── menu.html         # Menu page
│   └── utils/
│       ├── helpers.py        # Utility functions
│       └── decorators.py     # Custom decorators
├── babel.cfg                 # Babel configuration
├── requirements.txt          # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///restaurant_menu.db
```

### Admin Commands

```bash
# Initialize database
flask init-db

# Create new admin user
flask create-admin
```

## 🌐 Deployment

### Heroku Deployment

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

## 🛠️ Development

### Adding New Languages

1. Extract messages: `pybabel extract -F babel.cfg -o messages.pot .`
2. Create new translation: `pybabel init -i messages.pot -d app/translations -l <language_code>`
3. Translate messages in `app/translations/<language_code>/LC_MESSAGES/messages.po`
4. Compile translations: `pybabel compile -d app/translations`

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

## 📱 Screenshots

### Customer View
- Modern, responsive menu interface
- Category-based navigation
- Product search functionality
- Bilingual support

### Admin Panel
- Dashboard with statistics
- Category and product management
- Settings customization
- User-friendly interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Hossam Mekawy**
- GitHub: [@hossmekawy](https://github.com/hossmekawy)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Tailwind CSS for the utility-first CSS framework
- Alpine.js for reactive components
- All contributors and testers

## 📞 Support

If you have any questions or need help, please:
1. Check the [Issues](https://github.com/hossmekawy/advanced-retail-menu/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your setup and the issue

---

⭐ **Star this repository if you find it helpful!**
```

```gitignore:.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be added to the global gitignore or merged into this project gitignore.  For a PyCharm
#  project, it is common to ignore the files in the .idea/ directory.
.idea/

# VS Code
.vscode/

# Database files
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
*.tmp
*.temp
*~

# Application specific
uploads/
static/uploads/
```

```txt:LICENSE
MIT License

Copyright (c) 2024 Hossam Mekawy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Now run these commands to push everything to your GitHub repository:

```bash
git add README.md .gitignore LICENSE
```

```bash
git commit -m "Add documentation and project files

- Add comprehensive README with setup instructions
- Add .gitignore for Python projects
- Add MIT license
- Include deployment guides for Heroku and Railway
- Add development guidelines and contribution instructions"
```

```bash
git push origin main
