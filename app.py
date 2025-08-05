import requests
import streamlit as st
import os

st.title("📝 Auto README Generator from GitHub URL")

GITHUB_API = "GITHUB_API"

def get_repo_info(repo_url, token=None):
    try:
        repo_path = "/".join(repo_url.strip("/").split("/")[-2:])
        headers = {"Authorization": f"token {token}"} if token else {}
        repo_response = requests.get(f"{GITHUB_API}/{repo_path}", headers=headers)
        languages_response = requests.get(f"{GITHUB_API}/{repo_path}/languages", headers=headers)

        if repo_response.status_code != 200:
            return None, "Repository not found or invalid URL/token."

        repo_data = repo_response.json()
        languages = ", ".join(languages_response.json().keys())

        readme_content = f"""# {repo_data['name']}

{repo_data['description']}

## 🛠️ Technologies Used
{languages}

## 📦 Installation
Clone the repository:
```
git clone {repo_data['html_url']}
```

## 🚀 Usage
Explain how to run or use the project here.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first.

## 📄 License
{repo_data.get('license', {}).get('name', 'Not specified')}
"""
        return readme_content, None
    except Exception as e:
        return None, str(e)

repo_url = st.text_input("Enter GitHub Repository URL")
token = st.text_input("Enter GitHub Token (Optional)", type="password")

if st.button("Generate README"):
    if repo_url:
        readme, error = get_repo_info(repo_url, token)
        if error:
            st.error(error)
        else:
            st.success("README Generated Successfully!")
            st.download_button("Download README.md", readme, file_name="README.md")
            st.code(readme)
    else:
        st.warning("Please enter a GitHub repository URL.")
