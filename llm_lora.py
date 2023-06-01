from typing import Optional, List, Any
from langchain.llms.base import LLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


class HuggingFaceLoraPipeline(LLM):
    model: Any
    tokenizer: Any

    def _llm_type(self) -> str:
        return 'rinna-ppo'

    def _gen_prompt(self, prompt):
         return f"""ユーザー: {prompt}
                システム: 
                """

    def _call(self, 
              prompt: str,
              stop: Optional[List[str]] = None,
              ) -> str:
        prompt = self._gen_prompt(prompt)
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        output_ids = self.model.generate(
            token_ids,
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            repetition_penalty=1.1,  
        )
        output = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
        output = output.replace("<NL>", "\n")
        return output
    

def get_llm():
    model_name = "rinna/japanese-gpt-neox-3.6b-instruction-ppo"

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=nf4_config, device_map="auto")    
    llm = HuggingFaceLoraPipeline(
        model=model,
        tokenizer=tokenizer
    )
    return llm