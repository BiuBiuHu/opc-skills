import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "site"
EN_PAGE = SITE / "index.html"
ZH_PAGE = SITE / "zh" / "index.html"
VERSION = (REPO / "VERSION").read_text(encoding="utf-8").strip()
PAGES_WORKFLOW = REPO / ".github" / "workflows" / "pages.yml"

CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9+._/-]*")
LEADING_SLASH_ASSET = re.compile(r"""(?:href|src)=["'](/[^"']+)["']""")

ALLOWED_PHRASES = tuple(
    sorted(
        (
            "OPC Skills",
            "opc-skills",
            "One PC",
            "Plugins Directory",
            "Agent Plugin",
            "Content Agent",
            "Loop Engineering",
            "Code Review",
            "OpenAI",
            "Codex",
            "Cursor",
            "Claude",
            "Vercel",
            "Cloudflare",
            "GitHub",
            "Python",
            "SKILL.md",
            "FEATURE_NAME",
            "Explorer",
            "Frontend",
            "Backend",
            "Integration",
            "DevOps",
            "Content",
            "English",
            "Agent",
            "Skills",
            "Skill",
            "spec/TDD",
            "MIT",
            "PRD",
            "API",
            "CLI",
            "App",
            "Web",
            "Git",
            "npx",
            "npm",
            "curl",
            "bash",
            "doctor",
            "install",
            "update",
            "path",
            "plugin",
            "marketplace",
            "curated",
            "openai/skills",
            "subagent",
            "subagents",
            "worktree",
            "commit",
            "deployment",
            "diff",
            "smoke",
            "worker",
            "mock",
            "spec",
            "TDD",
            "P0/P1",
            "MAJOR",
            "MINOR",
            "PATCH",
            "B-side",
            "C",
            "QA",
            "UI",
            "OPC",
        ),
        key=len,
        reverse=True,
    )
)

EN_MARKETING_ON_ZH = (
    "Who it is for",
    "What you get",
    "Further reading",
    "Skip to content",
    "View on GitHub",
    "From a pain point",
    "Ship the consumer",
    "solo builders",
    "This page is the product introduction",
    "Upgrade an existing install",
    "Keep it current",
    "When shipping a product",
    "Version from the change",
    "skill for coding agents",
    "Skill for coding agents",
    "Coding agents can use",
    "not only Codex",
    "A Codex Skill",
)

ZH_MARKETING_ON_EN = (
    "给谁用",
    "你会得到什么",
    "延伸阅读",
    "交付闭环",
    "从痛点",
    "跳到正文",
    "一人公司",
)


class VisibleTextParser(HTMLParser):
    SKIP_TAGS = {"script", "style", "pre", "code", "kbd", "samp", "noscript"}

    def __init__(self):
        super().__init__()
        self._skip = 0
        self._lang_switch = 0
        self.visible = []
        self.lang_switch = []
        self.hrefs = []
        self.srcs = []
        self.lang = ""
        self.ids = set()
        self.versions = []
        self.hreflang = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if "data-opc-version" in attrs:
            self._capturing_version = True
        if tag in self.SKIP_TAGS:
            self._skip += 1
        if "lang-switch" in classes:
            self._lang_switch += 1
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
            if attrs.get("hreflang"):
                self.hreflang[attrs["hreflang"]] = attrs["href"]
        if tag == "link" and attrs.get("rel") == "alternate" and attrs.get("hreflang") and attrs.get("href"):
            self.hreflang[attrs["hreflang"]] = attrs["href"]
        if attrs.get("src"):
            self.srcs.append(attrs["src"])
        if attrs.get("href") and tag == "link":
            self.hrefs.append(attrs["href"])
        if attrs.get("id"):
            self.ids.add(attrs["id"])

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip:
            self._skip -= 1
        if tag == "nav" and self._lang_switch:
            self._lang_switch -= 1
        if getattr(self, "_capturing_version", False) and tag in {"span", "strong", "b"}:
            self._capturing_version = False

    def handle_data(self, data):
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        if getattr(self, "_capturing_version", False):
            self.versions.append(text)
        if self._skip:
            return
        if self._lang_switch:
            self.lang_switch.append(text)
            return
        self.visible.append(text)


def parse(path: Path) -> VisibleTextParser:
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def strip_allowed(text: str) -> str:
    stripped = text
    for phrase in ALLOWED_PHRASES:
        stripped = re.sub(re.escape(phrase), " ", stripped, flags=re.I)
    stripped = re.sub(r"https?://\S+", " ", stripped)
    stripped = re.sub(r"v?\d+\.\d+(?:\.\d+)?", " ", stripped)
    stripped = re.sub(r"~/\S+", " ", stripped)
    return stripped


def leftover_english_runs(text: str) -> list[str]:
    stripped = strip_allowed(text)
    pattern = re.compile(r"(?:[A-Za-z][A-Za-z0-9+._/-]*[\s,;:：、/+\-–—'’]*){4,}")
    runs = []
    for match in pattern.finditer(stripped):
        chunk = match.group(0).strip()
        if len(EN_WORD_RE.findall(chunk)) >= 4:
            runs.append(chunk)
    return runs


class SiteTests(unittest.TestCase):
    def test_pages_exist(self):
        self.assertTrue(EN_PAGE.is_file())
        self.assertTrue(ZH_PAGE.is_file())
        self.assertTrue((SITE / "zh" / "index.html").is_file())

    def test_version_matches_repo(self):
        self.assertEqual((SITE / "version.txt").read_text(encoding="utf-8").strip(), VERSION)
        for path in (EN_PAGE, ZH_PAGE):
            parsed = parse(path)
            self.assertTrue(parsed.versions, path)
            self.assertTrue(all(item == VERSION for item in parsed.versions), parsed.versions)

    def test_language_attributes_and_switch(self):
        en = parse(EN_PAGE)
        zh = parse(ZH_PAGE)
        self.assertEqual(en.lang, "en")
        self.assertTrue(zh.lang.startswith("zh"))
        self.assertIn("English", en.lang_switch)
        self.assertIn("中文", en.lang_switch)
        self.assertIn("English", zh.lang_switch)
        self.assertIn("中文", zh.lang_switch)
        self.assertTrue(any(href in {"zh/", "./zh/", "zh/index.html"} for href in en.hrefs))
        self.assertTrue(any(href in {"../", "../index.html"} for href in zh.hrefs))

    def test_english_pages_have_no_chinese_marketing(self):
        html = EN_PAGE.read_text(encoding="utf-8")
        en = parse(EN_PAGE)
        body = " ".join(en.visible)
        self.assertFalse(CJK_RE.search(body), f"English page has Chinese copy: {CJK_RE.findall(body)}")
        for phrase in ZH_MARKETING_ON_EN:
            self.assertNotIn(phrase, html)

    def test_chinese_pages_have_no_english_marketing_sentences(self):
        html = ZH_PAGE.read_text(encoding="utf-8")
        zh = parse(ZH_PAGE)
        body = " ".join(zh.visible)
        for phrase in EN_MARKETING_ON_ZH:
            self.assertNotIn(phrase, html)
            self.assertNotIn(phrase, body)
        runs = leftover_english_runs(body)
        self.assertEqual(runs, [], f"Chinese page still has English marketing sentences: {runs}")

    def test_required_sections(self):
        for path in (EN_PAGE, ZH_PAGE):
            parsed = parse(path)
            for section_id in ("audience", "loop", "gain", "install", "reading"):
                self.assertIn(section_id, parsed.ids, path)

    def test_github_and_reading_links(self):
        en = parse(EN_PAGE)
        zh = parse(ZH_PAGE)
        self.assertIn("https://github.com/BiuBiuHu/opc-skills", en.hrefs)
        self.assertIn("https://github.com/BiuBiuHu/opc-skills", zh.hrefs)
        self.assertIn("https://www.peak-lake.com/en/blog/opc-software-practice/", en.hrefs)
        self.assertIn("https://www.peak-lake.com/en/blog/mslj4f6g/", en.hrefs)
        self.assertIn("https://www.peak-lake.com/blog/opc-software-practice/", zh.hrefs)
        self.assertIn("https://www.peak-lake.com/blog/mslj4f6g/", zh.hrefs)

    def test_base_path_safe_asset_urls(self):
        for path in (EN_PAGE, ZH_PAGE):
            html = path.read_text(encoding="utf-8")
            for match in LEADING_SLASH_ASSET.findall(html):
                self.assertTrue(
                    match.startswith("/opc-skills/") or match.startswith("#"),
                    f"{path} has a root-absolute URL that will break on GitHub Pages: {match}",
                )
            parsed = parse(path)
            for src in parsed.srcs:
                self.assertFalse(src.startswith("/"), src)
                self.assertIn("assets/", src)

    def test_not_claimed_as_public_plugin_directory(self):
        en = EN_PAGE.read_text(encoding="utf-8")
        zh = ZH_PAGE.read_text(encoding="utf-8")
        self.assertIn("not in the public Plugins Directory", en)
        self.assertIn("尚未进入公开 Plugins Directory", zh)
        self.assertNotIn("listed in the public Plugins Directory", en.lower())

    def test_pages_workflow_deploys_site_from_main(self):
        workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("path: site", workflow)
        self.assertIn("branches:", workflow)
        self.assertIn("main", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("python3 site/sync_version.py", workflow)

    def test_preview_uses_github_pages_base_path(self):
        source = (SITE / "preview.py").read_text(encoding="utf-8")
        self.assertIn('/opc-skills', source)

    def test_release_version_is_planned_from_change_type(self):
        en = EN_PAGE.read_text(encoding="utf-8")
        zh = ZH_PAGE.read_text(encoding="utf-8")
        self.assertIn(
            "When shipping a product, the skill plans the version from the change type",
            en,
        )
        self.assertIn("MAJOR", en)
        self.assertIn("MINOR", en)
        self.assertIn("PATCH", en)
        self.assertNotIn("automatic background updates", en)
        self.assertNotIn("automatic version bumping", en)
        self.assertNotIn("Upgrade an existing install to the latest version with one command", en)
        self.assertIn("发布产品时，skill 按这次用户可见变更的类型规划版本", zh)
        self.assertIn("MAJOR", zh)
        self.assertIn("MINOR", zh)
        self.assertIn("PATCH", zh)
        self.assertNotIn("一条命令即可把已安装的 skill 升到最新版本", zh)

    def test_positioned_for_coding_agents_not_codex_only(self):
        en = EN_PAGE.read_text(encoding="utf-8")
        zh = ZH_PAGE.read_text(encoding="utf-8")
        self.assertIn("skill for coding agents", en)
        self.assertIn("Coding agents can use this skill, not only Codex", en)
        self.assertNotIn("is a Codex Skill", en)
        self.assertNotIn("A Codex Skill", en)
        self.assertIn("编程 Agent 都能用", zh)
        self.assertIn("不限于 Codex", zh)
        self.assertNotIn("是一套 Codex Skill", zh)
        self.assertNotIn("面向 C 端业务研发的 Codex Skill", zh)

    def test_language_guard_detects_mixed_copy(self):
        self.assertTrue(
            leftover_english_runs("这是一套 for shipping consumer apps 的说明"),
            "mixed English marketing on a Chinese page should fail",
        )
        self.assertFalse(CJK_RE.search("From a pain point to a shippable release."))
        self.assertTrue(CJK_RE.search("从痛点，做到可发布。"))


if __name__ == "__main__":
    unittest.main()
