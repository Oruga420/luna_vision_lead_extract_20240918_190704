import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_info_from_image(image_bytes):
    try:
        print(f"Processing image of size: {len(image_bytes)} bytes")
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        info_dict = {}
        fields = ['Company Name', 'Email', 'Name', 'Last Name', 'Phone', 'Extra Info']
        
        for field in fields:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Extract only the {field} from this image. Respond with only the extracted information, nothing else."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=50,
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            print(f"API response for {field}: {content}")
            info_dict[field] = content
        
        print(f"Extracted information: {info_dict}")
        return info_dict
    except Exception as e:
        print(f"Error in extract_info_from_image: {str(e)}")
        return {"error": "Failed to extract information from image"}
