# 规则索引

本目录包含安全加固 skill 的所有规则文件，执行前请按需加载：

| 规则文件 | 说明 | 何时加载 |
| --- | --- | --- |
| `boundary-system.md` | 三层边界系统（始终执行、先询问、永远不做） | 实现安全相关功能时读 |
| `owasp-prevention.md` | OWASP Top 10 预防（注入、认证、XSS、访问控制等） | 实现安全防护时读 |
| `input-validation.md` | 输入验证模式（模式验证、文件上传安全） | 处理用户输入时读 |
| `secrets-management.md` | 机密管理（环境变量、.gitignore 配置） | 处理敏感数据时读 |
| `security-checklist.md` | 安全审查清单 | 审查安全相关代码时读 |
