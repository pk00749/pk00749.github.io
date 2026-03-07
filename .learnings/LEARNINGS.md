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

## 类别 (category)

- `correction` - 用户纠正了我
- `knowledge_gap` - 知识过时或缺失
- `best_practice` - 发现了更好的方法

---
