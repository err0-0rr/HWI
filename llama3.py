# Use the native inference API to send a text message to Meta Llama 3.

import boto3
import json

from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime",
                             aws_access_key_id="",
                             aws_secret_access_key="",
                             region_name="us-east-1",
                             )
# Set the model ID, e.g., Llama 3 8b Instruct.
model_id = "meta.llama3-8b-instruct-v1:0"




# Extract and print the response text.
def test():
    prompt = "Act as a Shakespeare and write a poem on Genertaive AI"
    request = json.dumps(native_request)

    formatted_prompt = f"""
    <|begin_of_text|>
    <|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
    }

    try:
        response = client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)
    model_response = json.loads(response["body"].read())
    response_text = model_response["generation"]
    return response_text


