import requests

def retrieve_github_repo_contents(owner, repo_name, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                yield item
            elif item['type'] == 'dir':
                yield from retrieve_github_repo_contents(owner, repo_name, item['path'])
    else:
        return None

def save_to_txt_file(contents, file_name):
    with open(file_name, 'w') as file:
        for item in contents:
            file_url = item['download_url']
            file_content = requests.get(file_url).text
            file.write(f"File: {item['path']}\n")
            file.write(file_content)
            file.write("\n\n")

owner = ""
repo_name = ""
contents = retrieve_github_repo_contents(owner, repo_name)

if contents:
    save_to_txt_file(contents, "github_repo_contents.txt")
    print("Repository contents saved to github_repo_contents.txt")
else:
    print("Failed to retrieve repository contents")
