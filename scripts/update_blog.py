import feedparser
import git
import os

# Velog RSS 피드 URL (아이디를 supi001로 설정)
rss_url = 'https://api.velog.io/rss/@supi001'

# GitHub 레포지토리 경로 (현재 디렉터리 기준)
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 로컬 Git 저장소 로드
repo = git.Repo(repo_path)

# Git 사용자 정보 설정
config_writer = repo.config_writer(config_level='global')
config_writer.set_value('user', 'name', 'github-actions[bot]')
config_writer.set_value('user', 'email', 'github-actions[bot]@users.noreply.github.com')
config_writer.release()

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    file_name = entry.title.replace('/', '-').replace('\\', '-') + '.md'
    file_path = os.path.join(posts_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)

        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

# → 더 이상 repo.git.push() 호출하지 않음
