import feedparser
import git
import os

# Velog RSS 피드 URL (아이디를 supi001로 설정)
rss_url = 'https://api.velog.io/rss/@supi001'

# GitHub 레포지토리 경로 (현재 디렉터리 기준)
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 로컬 Git 저장소 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 파일명에 유효하지 않은 문자 대체
    file_name = entry.title.replace('/', '-').replace('\\', '-')
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # 파일이 존재하지 않으면 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)

        # Git 커밋
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

# 변경 사항을 원격에 푸시
repo.git.push()
