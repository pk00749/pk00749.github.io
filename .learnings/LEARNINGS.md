# LEARNINGS.md - 记录学到的新知识、纠正和最佳实践

## 记录格式

```
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述

### Details
完整背景：发生了什么、哪里错了、正确的应该是什么

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (如果与现有条目相关)
- Pattern-Key: xxx (可选，用于重复模式跟踪)
- Recurrence-Count: 1 (可选)
```

---

## [LRN-20260308-001] best_practice

**Logged**: 2026-03-08T00:08:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Hugo Stack Theme 需要 0.157.0+ 版本，版本不匹配会导致模板错误

### Details
Stack Theme 的 `widgets` 功能使用了 Hugo 0.157.0+ 的新 API（如 `IsImageResourceWithMeta`）。
当使用 0.156.0 版本时，构建会报错：
```
can't evaluate field IsImageResourceWithMeta in type interface {}
```

### Suggested Action
1. 安装主题前检查 `theme.toml` 中的 `min_version` 要求
2. 使用 `hugo version` 验证版本
3. 升级命令：
```bash
cd /tmp
wget https://github.com/gohugoio/hugo/releases/download/v0.157.0/hugo_extended_0.157.0_Linux-64bit.tar.gz
tar -xzf hugo.tar.gz
sudo mv hugo /usr/local/bin/
```

### Metadata
- Source: error
- Related Files: `/home/ubuntu/.openclaw/workspace-coder/projects/hugo-blog/themes/stack/theme.toml`
- Tags: hugo, version, compatibility, stack-theme
- Pattern-Key: hugo.version_check

## 类别 (category)

- `correction` - 用户纠正了我
- `knowledge_gap` - 知识过时或缺失
- `best_practice` - 发现了更好的方法

---
