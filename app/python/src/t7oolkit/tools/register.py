from t7oolkit.registry.tool_registry import registry
from t7oolkit.tools.demo_text_tool import DemoTextTool
from t7oolkit.tools.img_rect640_tool import ImgRect640Tool


def register_all_tools() -> None:
    registry.register(DemoTextTool())
    registry.register(ImgRect640Tool())
