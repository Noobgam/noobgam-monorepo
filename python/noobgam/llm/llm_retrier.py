import logging
from typing import Callable, Optional

from noobgam.llm.chain import ConversationHistoryChain


def retry_until_valid(
    retries: int,
    chain: ConversationHistoryChain,
    prompt: str,
    validator: Callable[[str], Optional[str]] = lambda x: None,
):
    response = chain.invokes(prompt)
    logging.info(f"Got response {response} from LLM")
    reprompt = validator(response)
    if not reprompt:
        return response
    else:
        logging.warning(f"Could not get a response, will reprompt {reprompt}")

    for retry_number in range(retries):
        response = chain.invokes(reprompt)
        reprompt = validator(response)

        if not reprompt:
            return response
        else:
            logging.warning(f"Could not get a response, will reprompt {reprompt}")

    raise Exception("Couldn't get valid response")
