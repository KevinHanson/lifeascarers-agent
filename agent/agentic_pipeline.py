import os, requests, json, datetime
from langchain_ollama import OllamaLLM

# 1️⃣ Connect to local Ollama model
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
llm = OllamaLLM(model="mistral", base_url=OLLAMA_API_URL)  # uses your running Ollama container

# 2️⃣ Fetch new works from Dimensions API
def fetch_dimensions_papers():
    DIMENSIONS_API_KEY = os.getenv("DIMENSIONS_API_KEY")
    if not DIMENSIONS_API_KEY:
        raise ValueError("Missing Dimensions API key. Please set DIMENSIONS_API_KEY environment variable.")

    # Authenticate
    auth_url = "https://app.dimensions.ai/api/auth.json"
    auth_resp = requests.post(auth_url, json={"key": DIMENSIONS_API_KEY}, timeout=30)
    auth_resp.raise_for_status()
    token = auth_resp.json().get("token")
    headers = {"Authorization": f"JWT {token}"}

    # Build DSL query for the last 7 days
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    query = f"""
    search publications in title_abstract_only for
    "((care partner~3) OR caregiver* OR caregiving OR carer*) AND (dementia OR alzheimer* OR ADRD)"
    where
    date >= "{week_ago}"
    and date <= "{today}"
    return publications[title + abstract + authors + date + doi + journal + linkout]
    """

    # Query the Dimensions DSL API
    resp = requests.post(
        "https://app.dimensions.ai/api/dsl.json",
        data=query.encode("utf-8"),  # <-- plain text DSL
        headers=headers,
        timeout=60
    )


    if resp.status_code != 200:
        print("❌ Dimensions API error:", resp.text)
        resp.raise_for_status()

    results = resp.json().get("publications", [])
    if not results:
        print("⚠️ No recent open-access caregiving papers found.")
        return []
    return results


# 3️⃣ Summarize each paper in the LifeAsCarers voice
def summarize_paper(title, abstract, authors=None, date=None):
    author_list = ", ".join(authors) if authors else "N/A"
    prompt = f"""
You are writing as part of the LifeAsCarers project—a blog that translates new dementia research
into meaningful, hopeful insights for care partners, family members, and educators.

Audience: non-technical caregivers who want to understand how new research can improve daily life.

Tone: warm, compassionate, educational, and empowering. Avoid jargon and maintain an uplifting,
human-centered voice.

Structure your post as follows:
1. **Opening (2–3 sentences):** a relatable or reflective introduction that connects emotionally to caregiving.
2. **Research Summary (2–3 short paragraphs):** what the study explored, how it was done, and what was found.
3. **Practical Reflection (1 paragraph):** how this insight might support care partners or educators in real life.
4. **Takeaway for Care Partners (1–2 sentences):** a concise, positive message in bold.

Paper details:
- Title: {title}
- Authors: {author_list}
- Publication Date: {date}
- Abstract: {abstract}

Write the response in Markdown for a blog post. Do not include citations or references.
"""
    return llm.invoke(prompt)  # ✅ modern call interface


# 4️⃣ Run the main agent loop
def main():
    print("🔍 Fetching new dementia caregiving papers from Dimensions...")
    papers = fetch_dimensions_papers()
    if not papers:
        print("✅ No new papers found for this period.")
        return

    summaries = []
    for paper in papers[:3]:  # limit for testing; increase as needed
        title = paper.get("title")
        abstract = paper.get("abstract")
        if not abstract:
            continue

        authors = [a.get("name") for a in paper.get("authors", []) if a.get("name")]
        date = paper.get("date", "Unknown")
        doi = paper.get("doi", "")
        linkout = paper.get("linkout", "")
        journal = paper.get("journal", "")

        summary = summarize_paper(title, abstract, authors, date)

        # Add attribution footer
        footer = "\n\n---\n"
        footer += f"**Source:** {journal or 'Unknown Journal'}  \n"
        if doi or linkout:
            footer += f"[{doi or 'Read the full paper'}]({linkout or '#'})\n"
        summary += footer

        summaries.append({"title": title, "summary": summary})
        print(f"\n📝 {title}\n{summary}\n")

    # 5️⃣ Save each summary as a Markdown blog post
    output_dir = "data/posts"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.date.today().strftime("%Y-%m-%d")

    for post in summaries:
        safe_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in post["title"])
        safe_title = safe_title.strip().replace(" ", "-").lower()[:60]
        filename = f"{timestamp}-{safe_title}.md"
        path = os.path.join(output_dir, filename)

        # Optional YAML front matter for CMS/blog publishing
        front_matter = f"""---
title: "{post['title']}"
date: {timestamp}
tags: ["dementia", "caregiving", "research", "lifeascarers"]
author: "LifeAsCarers AI Agent"
---

"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(front_matter + post["summary"] + "\n")

    # 6️⃣ Save a JSON log
    os.makedirs("data", exist_ok=True)
    with open("data/summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)

    print(f"\n✅ Saved {len(summaries)} LifeAsCarers blog posts to {output_dir}/")


if __name__ == "__main__":
    main()
