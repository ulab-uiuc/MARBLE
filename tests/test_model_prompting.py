import unittest

from litellm.types.utils import Message

from marble.llms.model_prompting import model_prompting


class TestModelPrompting(unittest.TestCase):
    def test_model_prompting(self) -> None:
        prompt = "This is a test sentence."
        message = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role":"system", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None
        )[0]
        self.assertIsInstance(message, Message)

if __name__ == '__main__':
    unittest.main()
