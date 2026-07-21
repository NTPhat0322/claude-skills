# claude-skills — Hướng dẫn

Repo cung cấp thư mục **`.claude/`** (skills, rules, commands, agents, hooks, …) để **copy vào project** và dùng trong **Claude Code**. Cấu trúc & cách dùng từng phần: **[`.claude/README.md`](.claude/README.md)**.

Đây là bản port sang Claude Code của kit `cursor-skills` (thư mục `../cursor-skills` cạnh repo này) — cùng nội dung, dùng đúng cơ chế native của Claude Code: skills tự động phát hiện dưới `.claude/skills/`, slash command namespaced (`/ck:cook`), sub-agent dưới `.claude/agents/`, và hook Python đăng ký qua `.claude/settings.json` (đã kèm sẵn, không cần cấu hình thêm như Cursor).

**Đã copy `.claude/` vào repo đích?** Làm **Checklist** (bước 1→6).

---

## Kit này dùng để làm gì?

Thay vì bảo Claude "code tính năng X" và nhận về kết quả không rõ ràng, kit này ép quy trình đi qua các bước có kiểm soát — **plan → code → test → review → commit** — với sub-agent chuyên trách từng bước, để bạn luôn biết Claude đang ở bước nào và có thể can thiệp.

**Luồng pipeline `ck` ví dụ:**

```
/ck:brainstorm → spec.md
/ck:plan --hard spec.md → plans/{slug}/plan.md + phase-01.md, phase-02.md, ...
/ck:cook plans/{slug}/plan.md → code từng phase, tự gọi tester + code-reviewer + git-manager
/ck:fix (khi có bug) → scout (thu thập bằng chứng) → debugger (chẩn đoán + fix) → review → commit
```

Mỗi lệnh có **mode**: `--fast` / `--quick` (bỏ qua test/review, làm nhanh), `--hard` (bắt buộc người duyệt, không auto-approve), mặc định **Standard** (tự approve nếu điểm review ≥ 9.5 và 0 lỗi CRITICAL).

**Agent dùng chung** (`.claude/agents/*.md`), điều phối bởi các lệnh `/ck:*` — không tự gọi trực tiếp trừ khi bạn muốn:
- `planner`, `plan-reviewer`, `researcher` — dùng trong `/ck:plan`
- `scout`, `debugger` — dùng trong `/ck:fix`
- `tester`, `code-reviewer` — dùng trong cả `/ck:cook` và `/ck:fix`
- `project-manager`, `docs-manager`, `git-manager` — bộ ba "finalize" dùng chung ở bước cuối mọi pipeline (cập nhật plan, cập nhật docs, commit git)

**Hooks tự động** (`.claude/hooks/*.py`, đăng ký sẵn trong `settings.json`) chạy theo sự kiện Claude Code thật, không phải do model tự quyết: `privacy_block.py` chặn đọc file secrets, `build_check.py` tự build/type-check sau khi sửa file, `simplify_gate.py` tự kích hoạt skill dọn code khi edit quá nhiều, cùng các hook lưu/nạp trạng thái phiên. Chi tiết đầy đủ: **[`.claude/hooks/README.md`](.claude/hooks/README.md)**.

**Skills độc lập khác** (ngoài pipeline `ck`): `skill-creator` (tạo skill mới), `code-review`, `problem-solving`, `sequential-thinking`, `mermaidjs-v11`, `playwright-skill`, `backend-mindset`, `strategic-compact`, `caveman`.

**Rules** (`.claude/rules/ck-*-design.md`) không tự nạp — chỉ tham chiếu khi *tạo mới* hoặc *review* một agent/command/skill để giữ nhất quán với kit (một việc một agent, command chỉ điều phối, skill dưới 500 dòng, …).

---

## Lấy kit và copy

Từ máy bạn cần có thư mục `./.claude/` (clone repo này hoặc copy từ monorepo).

```bash
rsync -a ./.claude/ /đường/dẫn/project/.claude/
```

*(Tuỳ chọn)* Gộp skill vào mọi project (`~/.claude/skills/`): `./scripts/sync-skills-to-home.sh`.

---

## Checklist — sau khi copy

| # | Việc làm |
|---|----------|
| **1** | `.claude/` nằm **ngay root** project (cùng cấp `.git` / `package.json`). `ls .claude` có `skills`, `commands`, `agents`, `hooks`, `settings.json`, … |
| **2** | Mở Claude Code (CLI `claude`, desktop app, hoặc IDE extension) đúng tại root đó. Monorepo: mở app con có `.claude/`, không mở cha. |
| **3** | Nếu đã mở project **trước** khi copy: khởi động lại phiên (`/clear` hoặc mở lại `claude`) để `settings.json` và hooks được nạp. |
| **4** | Gõ **`/`** → thử `/ck:plan`, `/ck:cook`, … Các lệnh nằm dưới `.claude/commands/ck/*.md`, hiện dưới dạng `/ck:<name>` (namespace theo thư mục). |
| **5** | **`@`** tới `.claude/skills/.../SKILL.md` để tham chiếu trực tiếp, hoặc để Claude tự trigger theo `description` trong frontmatter. |
| **6** | Kiểm tra hooks đã đăng ký trong `.claude/settings.json` — chạy `python scripts/verify_kit.py` (nếu ở repo này) để xác nhận agents/commands/skills/hooks hợp lệ. |

Python 3.x cần có trong PATH để hooks chạy (`.claude/hooks/*.py`). Chi tiết: [`.claude/hooks/README.md`](.claude/hooks/README.md).

---

## Slash gợi ý (`ck`)

| Slash | Mục đích |
|-------|----------|
| `/ck:brainstorm` | Ý tưởng / spec |
| `/ck:plan` | Kế hoạch triển khai |
| `/ck:cook` | Code theo plan |
| `/ck:fix` | Sửa lỗi có quy trình |
| `/ck:code-review` | Review local hoặc PR |
| `/ck:docs-fe` | Sinh tài liệu handoff FE |
| `/ck:learn` | Trích xuất pattern thành skill mới |
| `/ck:show-off` | Sinh trang HTML trình chiếu + chụp ảnh |
| `/ck:coding-level` | Đặt mức độ giải thích code |
| `/ck:init` | Bootstrap `.claude` sang repo khác |

---

## Sự cố thường gặp

- **Không thấy `/ck:*`:** sai workspace, chưa reload session, hoặc file lệnh không nằm đúng `commands/ck/*.md`.
- **Hook `.py` không chạy:** kiểm tra Python 3 có trong PATH và `.claude/settings.json` có đăng ký đúng script + event.

---

## Trong repo `claude-skills` (maintainer)

```bash
python scripts/verify_kit.py
```

Ghi chú: kit này được port thủ công từ `cursor-skills` (đổi `.cursor/` → `.claude/`, namespace hoá commands, chuyển `tools:` sang định dạng chuỗi của Claude Code, chuyển rules `.mdc` sang tài liệu tham chiếu `.md`). Khi đồng bộ nội dung skill mới từ `cursor-skills`, áp dụng lại các bước đó thay vì copy thẳng.
