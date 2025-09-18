import os
import hashlib
from datetime import datetime

CONTENT_DIR = "content/posts"

for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue
        path = os.path.join(root, file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 找到 front matter 边界
        if lines[0].strip() != "---":
            continue  # 没有 front matter
        try:
            end_index = lines[1:].index("---\n") + 1
        except ValueError:
            continue  # 不完整 front matter

        front_matter = lines[1:end_index]

        # 检查是否已有 slug
        if any(line.strip().startswith("slug:") for line in front_matter):
            continue

        # 找日期和标题生成 slug
        date_str = None
        title = None
        for line in front_matter:
            if line.startswith("date:"):
                date_str = line[len("date:"):].strip()
            if line.startswith("title:"):
                title = line[len("title:"):].strip()

        if not date_str:
            date_str = datetime.now().isoformat()
        if not title:
            title = file.replace(".md", "")

        combined = f"{date_str}{title}"
        import hashlib
        md5_hash = hashlib.md5(combined.encode("utf-8")).hexdigest()
        slug = md5_hash[3:11]

        # 插入 slug（直接插入到 front matter 末尾）
        front_matter.append(f"slug: {slug}\n")

        # 写回文件
        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.writelines(front_matter)
            f.write("---\n")
            f.writelines(lines[end_index + 1:])

        print(f"Updated {file} → slug: {slug}")
