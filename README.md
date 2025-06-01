# Whisper Transcriber Plugin

使用 OpenAI Whisper 模型 + FastAPI 搭建的视频语音转文字 API 插件，适用于 Render 部署并集成进 Coze 智能体。

## 使用方法

1. 将本项目上传到你的 GitHub；
2. 在 [Render](https://render.com) 上新建 Web Service，连接你的仓库；
3. Coze 插件 Skill 设置如下：

- 请求 URL: `https://你的域名/transcribe`
- 方法: POST
- Body: { "video_url": "{{video_url}}" }

4. 响应结果即为视频语音内容。