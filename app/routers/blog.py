import os
import markdown
import frontmatter
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/blog", tags=["blog"])
templates = Jinja2Templates(directory="app/templates")

# This finds the 'content' folder relative to the current file location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content")

@router.get("/")
async def list_posts(request: Request):
    posts = []
    if os.path.exists(CONTENT_DIR):
        for category in os.listdir(CONTENT_DIR):
            cat_path = os.path.join(CONTENT_DIR, category)
            if os.path.isdir(cat_path):
                for file in os.listdir(cat_path):
                    if file.endswith(".md"):
                        with open(os.path.join(cat_path, file), "r", encoding="utf-8") as f:
                            post = frontmatter.load(f)
                            posts.append({
                                "title": post.get("title", file),
                                "date": post.get("date", "2025"),
                                "category": category,
                                "slug": file.replace(".md", ""),
                                "summary": post.get("summary", f"Research in {category}")
                            })
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts})

@router.get("/{category}/{slug}")
async def get_post(request: Request, category: str, slug: str):
    path = os.path.join(CONTENT_DIR, category, f"{slug}.md")
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Post not found")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
            # 'extra' and 'fenced_code' ensure code blocks and tables look good
            html_content = markdown.markdown(post.content, extensions=['extra', 'fenced_code', 'codehilite'])
            
        return templates.TemplateResponse("post.html", {
            "request": request,
            "content": html_content,
            "title": post.get("title", "Research Detail"),
            "date": post.get("date", "2025")
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))