#from pipelines import pipeline
#from main import extracted_text
from model_ import load_model
import json
#nlp=pipeline("question-generation",model="valhalla/t5-base-qg-hl")    
#print(nlp(extracted_text))

mod=load_model()
prompt="""Provide a detailed and accurate list of libraries located in burdwan,West Bengal, India,

Each response must:
1. Contain verified and valid names of libraries that are correctly recognized.
2. Ensure the information provided (name, description, latitude, longitude, and Google Maps link) is reliable and consistent with real-world data.

The response should be returned in the following JSON format:
[
    {
        "name": "Name of the library (must be accurately recognized)",
        "description": "A brief and accurate description of the library",
        "latitude": "Latitude coordinate of the library",
        "longitude": "Longitude coordinate of the library",
        "link": "Google Maps link for route directions to the library"
    },
    ...
]

If no libraries exist in the specified area, clearly state: "No libraries found for the provided PIN code."

Additional Instructions:
- Use reliable data sources for validation.
- Prioritize accuracy in place recognition, especially for names of libraries.

"""
response=mod.generate_content(prompt).text
extracted=json.loads(response)
print(extracted)
print(len(extracted))

