---
name: openspec-developer
description: 基于OpenSpec的自动化开发流程 - 根据用户需求自动生成变更并完成开发，无需询问
---

# OpenSpec 自动化开发者

根据用户需求自动运用 OpenSpec 生成变更提案并完成开发。

## 核心原则

1. **不询问用户** - 自主决策，保持开发势头
2. **使用 OpenSpec** - 所有变更通过 openspec-cn 管理
3. **自动生成产出物** - 创建 proposal.md, design.md, tasks.md

## 工作流程

### 1. 分析需求

用户给出需求后，自主分析：
- 功能模块
- 技术方案
- 实现步骤

### 2. 生成变更

```bash
# 在项目目录中
cd <项目目录>

# 创建变更 (kebab-case名称)
npx openspec-cn new change "<change-name>"
```

### 3. 创建产出物

根据 Schema 生成三个产出物：

**proposal.md** - 是什么和为什么
```markdown
# <变更名称>

## 问题/需求
<描述用户需求>

## 解决方案
<描述解决方案>

## 预期结果
<描述完成后的效果>
```

**design.md** - 如何
```markdown
# <变更名称> 设计

## 技术方案
<技术实现方案>

## 数据结构
<如有需要>

## API 设计
<如有需要>

## 界面设计
<如有需要>
```

**tasks.md** - 实现步骤
```markdown
# <变更名称> 实现任务

## 任务列表
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3
```

### 4. 执行实现

按照 tasks.md 执行开发，完成后更新 SPEC.md（如有）。

### 5. 提交代码

```bash
git add -A
git commit -m "feat: <变更描述>"
git push origin main
```

## 常用命令

```bash
# 列出所有变更
npx openspec-cn list

# 查看变更状态
npx openspec-cn status --change "<name>"

# 验证变更
npx openspec-cn validate --change "<name>"
```

## 注意事项

- 保持产出物简洁，避免过度设计
- 如遇不确定技术问题，自主决定最优方案
- 完成后及时提交代码
