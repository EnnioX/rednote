# Circe 配图制作 SOP

本文档记录制图操作细节。图片的内容结构和交付标准以 `CLAUDE.md` 第 7 节为准。

## 1. 输出规格

- PNG 尺寸：1080×1440，比例 3:4。
- PNG 输出到对应的 `posts/` 发布目录，SVG 源文件保留在 `assets/`。
- 发布稿不得嵌入 SVG。
- 每篇发布稿固定交付 5 张图片，编号依次为 `0-cover`、`1-industry-facts`、`2-supply-profit`、`3-catalysts`、`4-follow`。

## 2. 封面品牌合成

1. 生成只包含文字和装饰元素的 SVG，不在 SVG 中绘制头像或 Circe 文字。
2. 使用 `rsvg-convert` 将 SVG 导出为 PNG。
3. 使用 `assets/circe-branding.png`（380×330，透明底）合成到图片底部居中位置。
4. 使用 `PIL.Image.alpha_composite` 合成，不裁剪品牌图的透明通道。

圆形头像和账号名必须直接合成在最终 PNG 内。不得自行重画头像、圆框或账号文字。

## 3. 信息图品牌标

- industry-facts、supply-profit、catalysts 图片右上角均叠加 `assets/circe-branding.png`。
- 品牌图缩放至宽 280px 并保持宽高比，距顶部和右侧各 40px。
- 使用 `alpha_composite` 合成，不裁剪透明通道。

## 4. SVG 文字溢出检查

- 卡片可用宽度为 340px（总宽 420px，左右内边距各 40px）。
- font-size 26 时，纯中文不超过 12 字/行，混合中英文不超过 14 字符/行。
- 超长文本必须换行，并将卡片高度同步增加 30px。
- 避免在同一行放置过长的数字和符号组合，例如 `→ 50-100kW+`。
- 导出后运行 `bin/check_svg_overflow.py`，并人工检查文字是否被裁切、遮挡或超出卡片。

## 5. 固定品牌关注页

- 源模板：`assets/circe-follow.svg`。
- 固定成品：`assets/circe-follow.png`。
- 模板调整后，在项目根目录运行 `rsvg-convert -w 1080 -h 1440 assets/circe-follow.svg -o assets/circe-follow.png` 重新导出固定成品。
- 每篇发布稿直接复制固定成品到发布目录，并命名为 `20-N-4-follow.png`；不得为单篇发布稿重新生成、改写或重新设计。
- 头像和账号名位于上方显眼位置，下方以统一格式分三行展示“关注Circe”“用事实和数据”“跟踪市场真正的变化”，并保留“PUBLIC MATERIALS · DATA · SIGNALS”。
- 不得增加具体标的、荐股、收益暗示、私域引流或当期主题营销文案。
- 复制后检查 PNG 为 1080×1440，并在手机预览尺寸确认头像、账号名和关注文案清晰可读。
