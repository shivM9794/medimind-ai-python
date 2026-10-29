
import boto3

from app.core.config import settings


class BedrockAdapter:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
        )
        self.model_id = settings.bedrock_model_id

    def generate(self, question: str, context: str) -> str:
        if not self.model_id:
            raise RuntimeError(
                "Set BEDROCK_MODEL_ID in your .env file first."
            )

        response = self.client.converse(
            modelId=self.model_id,
            system=[
                {
                    "text": (
                        "You provide general health information. "
                        "Do not diagnose, prescribe, or recommend changing "
                        "prescribed medication. Use only relevant supplied "
                        "context, state when information is insufficient, "
                        "and advise consulting a qualified clinician for "
                        "personal medical decisions. For emergencies, "
                        "tell the user to contact local emergency services."
                    )
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": (
                                f"Question:\n{question}\n\n"
                                f"Reference context:\n{context}"
                            )
                        }
                    ],
                }
            ],
            inferenceConfig={
                "maxTokens": 700,
                "temperature": 0.2,
            },
        )

        content = response["output"]["message"]["content"]
        return "\n".join(
            item["text"] for item in content if "text" in item
        )
