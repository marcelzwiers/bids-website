from pathlib import Path
from rich import print

root = Path(__file__).parents[1] 

input_folder = root / "docs" / "website" / "_posts"
output_folder = root / "docs" / "blog" / "posts"
output_folder.mkdir(exist_ok=True)

for file in input_folder.glob("*.md"):
    print(file)

    tokens = file.name.split("-")

    year = tokens[0]
    month = tokens[1]
    day = tokens[2]

    title = "_".join(tokens[3:]).lower()
    title = title.replace(",", "")
    title = title.replace("_executive_summary", "")
    title = title.replace("_action_items_and", "")
    
    print(output_folder / f"{year}-{month}-{day}_{title}.md")

    with open(file, 'r') as f:
        content = f.readlines()
    
    with open(output_folder / f"{year}-{month}-{day}-{title}", 'w') as f:
        is_frontmatter = False
        frontmatter_done = False
        for line in content:

            if frontmatter_done:
                f.write(line.replace('{:target:"_blank"}', "").replace('{:target="_blank"}', ""))
                continue

            if line.startswith("---"):
                if not is_frontmatter:
                    is_frontmatter = True
                    f.write(line)
                    f.write(f"date: {year}-{month}-{day}\n")
                    continue
                else: 
                    is_frontmatter = False
                    frontmatter_done = True
                    f.write(line)
                    continue

            if is_frontmatter:
                if line.startswith("title"):
                    f.write(line.replace("title", "slug"))
                    continue
                if line.startswith("display"):
                    continue
                if line == "author:\n":
                    f.write("author: anonymous\n")
                    continue
                f.write(line)
                continue

    print("\n")            


# ---
# slug: "BIDS Community Survey 2024"
# date: 2024-03-01
# author: BIDS Maintainers
# display: true
# ---
