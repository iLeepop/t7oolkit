import type { Tool } from "../types/tool";
import { DemoTextTool } from "../tools/DemoTextTool";
import { ImgRect640Tool } from "../tools/ImgRect640Tool";

const tools: Tool[] = [];

export function registerTool(tool: Tool): void {
  tools.push(tool);
}

export function listTools(): Tool[] {
  return [...tools];
}

export function registerAllTools(): void {
  tools.length = 0;
  registerTool({
    id: "demo-text",
    name: "文本处理",
    description: "简单的文本输入/输出演示工具",
    component: DemoTextTool,
  });
  registerTool({
    id: "img-rect640",
    name: "图片缩放",
    description: "将文件夹内图片等比缩放至指定尺寸以内（默认 640×640）",
    component: ImgRect640Tool,
  });
}

registerAllTools();
