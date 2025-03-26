import json
import re

from pydantic import ValidationError

from regulus.agent.model import ImgRecognizeModel
from regulus.agent.prompt import load_prompt
from regulus.domain.quantor.model import ImgType
from regulus.domain.quantor.model.recognize_result import RecognizeResult


def extract_json_from_string(input_string: str) -> dict:
    """
    从输入字符串中提取被 ```json 和 ``` 包围的JSON部分，并解析为字典。

    :param input_string: 输入字符串
    :return: 解析后的JSON字典
    """
    # 使用正则表达式匹配 ```json 和 ``` 之间的内容
    pattern = r'```json(.*?)```'
    match = re.search(pattern, input_string, re.DOTALL)

    if not match:
        raise ValueError('未找到被 ```json 和 ``` 包围的JSON部分')

    # 提取匹配到的内容
    json_str = match.group(1).strip()

    try:
        # 将JSON字符串解析为字典
        result_dict = json.loads(json_str)
        return result_dict
    except json.JSONDecodeError as e:
        raise ValueError(f'JSON解析错误: {e}')


class ImgRecognizeService:

    def __init__(self, img_recognize_model: ImgRecognizeModel):
        self._img_recognize_model = img_recognize_model
        # todo 放到配置里
        self._prompt = load_prompt('img_recognize_prompt.md')

    def recognize(self, img_path) -> RecognizeResult:
        result_json = self._img_recognize_model(img_path, self._prompt)
        try:
            result_dict = self.extract_json_from_string(result_json)
            return RecognizeResult(type=ImgType(result_dict['type']),
                                   content=result_dict['content'])
        except ValidationError as e:
            print(f'验证错误: {e}')
            raise
        except json.JSONDecodeError as e:
            print(f'JSON解析错误: {e}')
            raise
