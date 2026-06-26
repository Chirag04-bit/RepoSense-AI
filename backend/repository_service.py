import os
import shutil
from git import Repo, GitCommandError
import json
import yaml

class RepositoryService:
    def __init__(self, base_dir="repositories"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def read_file_content(self, file_path, max_chars=None):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if max_chars:
                    return content[:max_chars]
                return content
        except Exception:
            return ""

    def clone_repository(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(self.base_dir, repo_name)

        if os.path.exists(repo_path):
            try:
                shutil.rmtree(repo_path)
            except PermissionError:
                print(f"Could not delete existing repository: {repo_path}")
                return repo_path

        try:
            Repo.clone_from(repo_url, repo_path)
            return repo_path
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")
            return None

    def _detect_framework(self, repo_path, file_extensions):
        framework = "Unknown"
        # Python frameworks
        if ".py" in file_extensions:
            if os.path.exists(os.path.join(repo_path, "manage.py")):
                framework = "Django"
            elif os.path.exists(os.path.join(repo_path, "app.py")) and "streamlit" in self.read_file_content(os.path.join(repo_path, "app.py"), 1000).lower():
                framework = "Streamlit"
            elif os.path.exists(os.path.join(repo_path, "app.py")) and "flask" in self.read_file_content(os.path.join(repo_path, "app.py"), 1000).lower():
                framework = "Flask"
            elif os.path.exists(os.path.join(repo_path, "main.py")) and "fastapi" in self.read_file_content(os.path.join(repo_path, "main.py"), 1000).lower():
                framework = "FastAPI"
        # JavaScript/TypeScript frameworks
        if ".js" in file_extensions or ".ts" in file_extensions:
            package_json_path = os.path.join(repo_path, "package.json")
            if os.path.exists(package_json_path):
                try:
                    with open(package_json_path, "r") as f:
                        package_json = json.load(f)
                    dependencies = package_json.get("dependencies", {})
                    dev_dependencies = package_json.get("devDependencies", {})
                    if "react" in dependencies or "react" in dev_dependencies:
                        framework = "React"
                    elif "angular" in dependencies or "angular" in dev_dependencies:
                        framework = "Angular"
                    elif "vue" in dependencies or "vue" in dev_dependencies:
                        framework = "Vue.js"
                    elif "express" in dependencies or "express" in dev_dependencies:
                        framework = "Express.js"
                    elif "next" in dependencies or "next" in dev_dependencies:
                        framework = "Next.js"
                    elif "nuxt" in dependencies or "nuxt" in dev_dependencies:
                        framework = "Nuxt.js"
                except json.JSONDecodeError:
                    pass
        # Java frameworks
        if ".java" in file_extensions:
            if os.path.exists(os.path.join(repo_path, "pom.xml")) and "spring-boot" in self.read_file_content(os.path.join(repo_path, "pom.xml"), 2000).lower():
                framework = "Spring Boot"
        
        return framework

    def _detect_orm(self, repo_path, all_files_content, file_extensions):
        orm = "None Detected"
        # Python ORMs
        if ".py" in file_extensions:
            if "sqlalchemy" in all_files_content.lower() or os.path.exists(os.path.join(repo_path, "alembic.ini")):
                orm = "SQLAlchemy"
            elif "django.db" in all_files_content.lower() or os.path.exists(os.path.join(repo_path, "manage.py")):
                orm = "Django ORM"
            elif "peewee" in all_files_content.lower():
                orm = "Peewee"
            elif "ponyorm" in all_files_content.lower():
                orm = "PonyORM"
        # JavaScript/TypeScript ORMs
        if ".js" in file_extensions or ".ts" in file_extensions:
            package_json_path = os.path.join(repo_path, "package.json")
            if os.path.exists(package_json_path):
                try:
                    with open(package_json_path, "r") as f:
                        package_json = json.load(f)
                    dependencies = package_json.get("dependencies", {})
                    dev_dependencies = package_json.get("devDependencies", {})
                    if "sequelize" in dependencies:
                        orm = "Sequelize"
                    elif "typeorm" in dependencies:
                        orm = "TypeORM"
                    elif "prisma" in dependencies:
                        orm = "Prisma"
                except json.JSONDecodeError:
                    pass
        # Java ORMs
        if ".java" in file_extensions:
            if "hibernate" in all_files_content.lower() or os.path.exists(os.path.join(repo_path, "src/main/resources/META-INF/persistence.xml")):
                orm = "Hibernate"
            elif "mybatis" in all_files_content.lower():
                orm = "MyBatis"
        return orm

    def _detect_database(self, repo_path, all_files_content):
        database = "None Detected"
        db_keywords = {
            "PostgreSQL": ["postgresql", "psycopg2", "pg_dump"],
            "MySQL": ["mysql", "mysqlclient", "pymysql"],
            "SQLite": ["sqlite", "sqlite3"],
            "MongoDB": ["mongodb", "pymongo"],
            "Redis": ["redis", "pyredis"],
            "SQL Server": ["mssql", "pyodbc"],
            "Oracle": ["oracle", "cx_oracle"],
        }

        for db_name, keywords in db_keywords.items():
            for keyword in keywords:
                if keyword in all_files_content.lower():
                    database = db_name
                    return database
        
        # Check for common database config files
        for root, _, files in os.walk(repo_path):
            for file in files:
                if "database" in file.lower() and (".yml" in file or ".json" in file or ".py" in file):
                    database = "Likely present (config file detected)"
                    return database
        return database

    def _detect_auth_library(self, repo_path, all_files_content, file_extensions):
        auth_library = "None Detected"
        # Python Auth
        if ".py" in file_extensions:
            if "django.contrib.auth" in all_files_content.lower() or "django-rest-framework-simplejwt" in all_files_content.lower():
                auth_library = "Django Auth / Simple JWT"
            elif "flask_login" in all_files_content.lower():
                auth_library = "Flask-Login"
            elif "fastapi_users" in all_files_content.lower():
                auth_library = "FastAPI Users"
        # JavaScript/TypeScript Auth
        if ".js" in file_extensions or ".ts" in file_extensions:
            package_json_path = os.path.join(repo_path, "package.json")
            if os.path.exists(package_json_path):
                try:
                    with open(package_json_path, "r") as f:
                        package_json = json.load(f)
                    dependencies = package_json.get("dependencies", {})
                    dev_dependencies = package_json.get("devDependencies", {})
                    if "passport" in dependencies:
                        auth_library = "Passport.js"
                    elif "next-auth" in dependencies:
                        auth_library = "NextAuth.js"
                    elif "firebase" in dependencies:
                        auth_library = "Firebase Auth"
                except json.JSONDecodeError:
                    pass
        return auth_library

    def _detect_build_tool(self, repo_path):
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            return "Maven"
        if os.path.exists(os.path.join(repo_path, "build.gradle")):
            return "Gradle"
        if os.path.exists(os.path.join(repo_path, "webpack.config.js")):
            return "Webpack"
        if os.path.exists(os.path.join(repo_path, "rollup.config.js")):
            return "Rollup"
        if os.path.exists(os.path.join(repo_path, "vite.config.js")):
            return "Vite"
        if os.path.exists(os.path.join(repo_path, "gulpfile.js")):
            return "Gulp"
        if os.path.exists(os.path.join(repo_path, "Gruntfile.js")):
            return "Grunt"
        return "None Detected"

    def _detect_testing_framework(self, repo_path, all_files_content, file_extensions):
        testing_framework = "None Detected"
        # Python Testing
        if ".py" in file_extensions:
            if "pytest" in all_files_content.lower() or os.path.exists(os.path.join(repo_path, "pytest.ini")):
                testing_framework = "Pytest"
            elif "unittest" in all_files_content.lower():
                testing_framework = "Unittest"
        # JavaScript/TypeScript Testing
        if ".js" in file_extensions or ".ts" in file_extensions:
            package_json_path = os.path.join(repo_path, "package.json")
            if os.path.exists(package_json_path):
                try:
                    with open(package_json_path, "r") as f:
                        package_json = json.load(f)
                    dependencies = package_json.get("dependencies", {})
                    dev_dependencies = package_json.get("devDependencies", {})
                    if "jest" in dependencies or "jest" in dev_dependencies:
                        testing_framework = "Jest"
                    elif "mocha" in dependencies or "mocha" in dev_dependencies:
                        testing_framework = "Mocha"
                    elif "cypress" in dependencies or "cypress" in dev_dependencies:
                        testing_framework = "Cypress"
                except json.JSONDecodeError:
                    pass
        # Java Testing
        if ".java" in file_extensions:
            if "junit" in all_files_content.lower():
                testing_framework = "JUnit"
            elif "mockito" in all_files_content.lower():
                testing_framework = "Mockito"
        return testing_framework

    def _detect_entry_point(self, repo_path, file_extensions):
        entry_points = {
            ".py": ["main.py", "app.py", "__init__.py"],
            ".js": ["index.js", "app.js", "server.js"],
            ".ts": ["index.ts", "app.ts", "server.ts"],
            ".java": ["Main.java"], # Heuristic, often main class
            ".go": ["main.go"],
            ".php": ["index.php"],
        }
        
        for ext, possible_entries in entry_points.items():
            if ext in file_extensions:
                for entry in possible_entries:
                    for root, _, files in os.walk(repo_path):
                        if entry in files:
                            return os.path.relpath(os.path.join(root, entry), repo_path)
        return "Unknown"

    def _detect_package_manager(self, repo_path):
        if os.path.exists(os.path.join(repo_path, "requirements.txt")):
            return "pip"
        if os.path.exists(os.path.join(repo_path, "package.json")):
            if os.path.exists(os.path.join(repo_path, "yarn.lock")):
                return "yarn"
            return "npm"
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            return "Maven"
        if os.path.exists(os.path.join(repo_path, "build.gradle")):
            return "Gradle"
        if os.path.exists(os.path.join(repo_path, "go.mod")):
            return "Go Modules"
        if os.path.exists(os.path.join(repo_path, "Gemfile")):
            return "Bundler"
        return "Unknown"

    def _detect_config_files(self, repo_path):
        config_files = []
        common_config_patterns = [
            "config", "settings", "env", "properties", "ini", "yaml", "yml", "json",
            "webpack", "babel", "tsconfig", "jest", "prettier", "eslint", "Dockerfile",
            "docker-compose", "Jenkinsfile", ".travis.yml", ".github",
        ]
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if any(pattern in file.lower() for pattern in common_config_patterns) or file.startswith(".") and file != ".gitignore":
                    config_files.append(os.path.relpath(os.path.join(root, file), repo_path))
        return config_files

    def _detect_readme_presence(self, repo_path):
        for file_name in ["README.md", "README.rst", "README.txt", "README"]:
            if os.path.exists(os.path.join(repo_path, file_name)):
                return True
        return False

    def _analyze_folder_hierarchy(self, repo_path, max_depth=3):
        hierarchy = []
        for root, dirs, files in os.walk(repo_path):
            level = root.replace(repo_path, "").count(os.sep)
            if level < max_depth:
                indent = "  " * level
                base_name = os.path.basename(root)
                if root == repo_path:
                    hierarchy.append(f"{base_name}/")
                else:
                    hierarchy.append(f"{indent}├── {base_name}/")
                for f in files:
                    hierarchy.append(f"{indent}│   ├── {f}")
        return "\n".join(hierarchy)

    def _generate_mermaid_diagram(self, folder_hierarchy):
        mermaid_diagram = ["graph TD"]
        lines = folder_hierarchy.split("\n")
        
        # Map to store folder paths and their corresponding Mermaid node IDs
        path_to_id = {"/": "root"}
        id_counter = 0

        # First pass: create nodes and map paths to IDs
        for line in lines:
            if "├──" in line or "└──" in line:
                parts = line.split(" ")
                level = 0
                for part in parts:
                    if part == "":
                        level += 1
                    else:
                        break
                
                folder_name = parts[-1].replace("/", "").strip()
                if not folder_name: # Skip empty folder names
                    continue

                current_path_parts = [p for p in parts if p not in ["", "├──", "└──"]]
                current_path = "/".join(current_path_parts)

                if current_path not in path_to_id:
                    id_counter += 1
                    path_to_id[current_path] = f"F{id_counter}"
                
                mermaid_diagram.append(f"    {path_to_id[current_path]}[{folder_name}]")

        # Second pass: create connections
        for i, line in enumerate(lines):
            if "├──" in line or "└──" in line:
                parts = line.split(" ")
                level = 0
                for part in parts:
                    if part == "":
                        level += 1
                    else:
                        break
                
                current_path_parts = [p for p in parts if p not in ["", "├──", "└──"]]
                current_path = "/".join(current_path_parts)

                if level > 0:
                    parent_path_parts = current_path_parts[:-1]
                    parent_path = "/".join(parent_path_parts)
                    if not parent_path: # Handle root level parents
                        parent_path = "/"

                    if parent_path in path_to_id and current_path in path_to_id:
                        mermaid_diagram.append(f"    {path_to_id[parent_path]} --> {path_to_id[current_path]}")

        return "\n".join(mermaid_diagram)

    def get_repository_info(self, repo_path):
        total_files = 0
        total_folders = 0
        file_extensions = {}
        all_files_content = ""

        ignore_dirs = [".git", "node_modules", "build", "dist", "__pycache__", "venv", ".venv"]

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            total_folders += len(dirs)
            for file in files:
                total_files += 1
                _, ext = os.path.splitext(file)
                if ext:
                    ext = ext.lower()
                    file_extensions[ext] = file_extensions.get(ext, 0) + 1
                
                file_content = self.read_file_content(os.path.join(root, file))
                all_files_content += file_content + "\n"

        main_language = self._get_main_language(file_extensions)
        framework = self._detect_framework(repo_path, file_extensions)
        database = self._detect_database(repo_path, all_files_content)
        orm = self._detect_orm(repo_path, all_files_content, file_extensions)
        auth_library = self._detect_auth_library(repo_path, all_files_content, file_extensions)
        build_tool = self._detect_build_tool(repo_path)
        testing_framework = self._detect_testing_framework(repo_path, all_files_content, file_extensions)
        entry_point = self._detect_entry_point(repo_path, file_extensions)
        config_files = self._detect_config_files(repo_path)
        package_manager = self._detect_package_manager(repo_path)
        readme_present = self._detect_readme_presence(repo_path)
        folder_hierarchy = self._analyze_folder_hierarchy(repo_path)

        return {
            "repo_name": os.path.basename(repo_path),
            "total_files": total_files,
            "total_folders": total_folders,
            "main_language": main_language,
            "framework": framework,
            "database": database,
            "orm": orm,
            "auth_library": auth_library,
            "build_tool": build_tool,
            "testing_framework": testing_framework,
            "entry_point": entry_point,
            "config_files": config_files,
            "package_manager": package_manager,
            "readme_present": readme_present,
            "folder_hierarchy": folder_hierarchy,
            "mermaid_diagram": self._generate_mermaid_diagram(folder_hierarchy),
            "all_files_content": all_files_content # This will be used for summary and other AI features
        }

    def _get_main_language(self, file_extensions):
        if file_extensions:
            # Exclude common non-programming file extensions for main language detection
            excluded_extensions = [".md", ".txt", ".json", ".xml", ".yaml", ".yml", ".css", ".html", ".scss", ".less", ".log", ".gitignore", ".env", ".example", ".lock", ".toml"]
            programming_extensions = {ext: count for ext, count in file_extensions.items() if ext not in excluded_extensions}
            if programming_extensions:
                return max(programming_extensions, key=programming_extensions.get).replace(".", "").capitalize()
            elif file_extensions:
                # Fallback to any extension if all programming extensions are excluded
                return max(file_extensions, key=file_extensions.get).replace(".", "").capitalize()
        return "Unknown"

    def read_source_code_files(self, repo_path):
        supported_extensions = [".py", ".js", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rb", ".php", ".swift", ".kt", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss", ".less", ".xml", ".json", ".yaml", ".yml", ".md"]
        ignore_dirs = [".git", "node_modules", "build", "dist", "__pycache__", "venv", ".venv"]
        
        source_files = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        content = self.read_file_content(file_path)
                        source_files.append({"file_path": file_path, "content": content})
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")
        return source_files
