class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def update(self, usage):
        """
        usage = response.usage
        """
        if not usage:
            return

        self.total_tokens += usage.total_tokens
        self.total_input_tokens += usage.prompt_tokens
        self.total_output_tokens += usage.completion_tokens

    def report(self):
        return {
            "total_tokens": self.total_tokens,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
        }

    def reset(self):
        self.total_tokens = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
