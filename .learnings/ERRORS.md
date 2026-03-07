# ERRORS.md - 记录命令失败和异常

## 记录格式

```
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述

### Error
```
实际错误信息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 环境详情

### Suggested Fix
如果可以识别，可能的解决方案

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (如果重复出现)
```

---
