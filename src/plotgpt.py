import pandas as pd
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from src.modules.utils import num_tokens_from_messages, _parse_code, _pandas_dtype_str, load_prompt
from typing import Tuple
from dotenv import load_dotenv
import os

load_dotenv()




class PlotGPT:
    def __init__(self, show_code: bool = True) -> None:
        self._llm = ChatOpenAI(model_name=os.getenv("_MODEL"))
        self._history = []
        self._system_prompt = load_prompt(os.getenv("_SYSTEM_TEMPLATE")).format(dtype_str=_pandas_dtype_str(pd.DataFrame()))
        print(self._system_prompt)
        self._human_prompt = load_prompt(os.getenv("_HUMAN_TEMPLATE"))
        self._show_code = show_code
        

    def _clear_history(self) -> None:
        self._history = []
        self._system_prompt = load_prompt(os.getenv("_SYSTEM_TEMPLATE")).format(dtype_str=_pandas_dtype_str(pd.DataFrame()))

    def inspect(self, df: pd.DataFrame) -> None:
        self._clear_history()
        self._system_prompt = SystemMessage(
            content=self._system_prompt.format(dtype_str=_pandas_dtype_str(df))
        )
        self._df = df

    def _construct_messages(self, new_msg: HumanMessage):

        return [self._system_prompt] +  [new_msg]

    def _get_response(self, prompt) -> Tuple[AIMessage, HumanMessage]:
        assert self._system_prompt is not None, "Inspect a dataframe first!"

        new_msg = HumanMessage(
            content= self._human_prompt.format(prompt  = prompt)
        )
        messages = self._construct_messages(new_msg)
        resp = self._llm(messages)
        print(messages, resp)
        return resp, new_msg

    def ask(self, prompt) -> None:
        assert self._system_prompt is not None, "Need to inspect a dataframe first!"

        ai_response, msg = self._get_response(prompt)
        self._history += [msg, ai_response]
        code = _parse_code(ai_response.content)
        if self._show_code:
            print(code)
        # TODO: try/ except plot
        exec(code, {"df": self._df})
    def get_code(self, prompt) -> None:
        assert self._system_prompt is not None, "Need to inspect a dataframe first!"

        ai_response, msg = self._get_response(prompt)
        self._history += [msg, ai_response]
        code = _parse_code(ai_response.content)
        return code

if __name__ == "__main__":

    ai = PlotGPT()
    ai.ask("plot sepal width vs sepal length")

    ai.ask("now color it by species")

    ai.ask("make separate sepal width vs sepal length scatterplot subplots per species. Combine it into a single figure")
