from typing import List, Optional, Sequence, Any
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema.language_model import BaseLanguageModel
# from langchain.agents.mrkl.prompt import SUFFIX
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.agents.agent import  AgentOutputParser
from Intelligence.dag_planner.templates_prompts import PREFIX, FORMAT_INSTRUCTIONS, SUFFIX
from langchain.chains.llm import LLMChain
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from Intelligence.utils.llm_utils import llm
from Intelligence.utils.misc_utils import logger

class PersonalAgent(ZeroShotAgent):
    

    @classmethod
    def create_prompt(
        cls,
        user_query: str ,
        tools: Sequence[BaseTool] ,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:

        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names)
        #________________________________________________________________________________



        template = "\n\n".join([prefix, tool_strings, format_instructions,  suffix])    # mistakes

        if input_variables is None:
            input_variables = ["input", "agent_scratchpad"]
        
        prompt =  PromptTemplate(template=template, input_variables=input_variables)
        
        # if user_query != None:
        #     prompt.template = prompt.template.format(input=user_query, agent_scratchpad='')
           
        return prompt
    #________________________________________________________________________________________________________________________________
    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        user_query: str = None,
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> 'PersonalAgent':
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)

        prompt = cls.create_prompt(
            tools=tools,
            prefix=prefix,
            user_query=user_query,
            suffix=suffix,
            format_instructions=format_instructions,
            input_variables=input_variables,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser()

        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )

#________________________________________________________________________________________________________________________________   
from Intelligence.dag_planner.tools import *
task_tools = [
    SearchObjectByName() ,
    GetSimilarWorkItems() , 
    Summarize() ,
    Prioritize(), 
    CreateActionableTasksFromText(), 
    DiabetesDoctor(),
    BPDoctor()
]

agent_obj = PersonalAgent.from_llm_and_tools(
            llm = llm, tools = task_tools, output_parser=ReActSingleInputOutputParser()
            )