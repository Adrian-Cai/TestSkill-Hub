# 最终交付契约

每个音频部分的项目至少包含：

```text
part-project/
├── standalone-preview.html
├── timeline.json 或 timeline(<part>).json
├── transcript.raw.json 或 transcript.raw(<part>).json
├── transcript.cleaned.txt（生成时提供）
├── alignment-report.json（发生校准时提供）
├── audio/
│   └── 原始或规范化音频
├── START_WINDOWS.bat
├── START_MAC_LINUX.sh
└── README.md
```

## HTML 必须满足

- 固定 1920×1080 逻辑画布。
- 浏览器窗口只做等比例缩放，不重新排版。
- 音频直接嵌入，或在项目中具备可验证的本地路径。
- 播放错误必须可见，不能静默失败。
- 支持 `record`、`autoplay`、`delay`、`guide` 和 `t` 参数。
- 动画状态由 `audio.currentTime` 决定，拖动后可以正确重建。
- 不使用外部 CDN 作为最终交付依赖。
- 录制舞台默认只保留旁白驱动的正文与必要图形；预览控制必须位于舞台外。
- 默认不显示品牌/课程名称、时钟、章节导航、cue 调试文案或进度条。
- 时间轴不包含全局标题、场景标题、眉题或摘要字段；没有当前 cue 时画面保持空白。
- 抽查每个场景的代表 cue：只显示当前 beat，上一 beat 已退场。

## ZIP 必须满足

- 解压后可启动。
- 不包含缓存目录、`node_modules`、临时音频或调试截图。
- 文件名清晰，音频部分编号保持一致。
