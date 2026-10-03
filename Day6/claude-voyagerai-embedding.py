import os
import voyageai
from dotenv import load_dotenv

load_dotenv()


vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
	  "Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]

documents_embeddings = vo.embed(documents, model="voyage-3.5", input_type="document").embeddings

print(len(documents_embeddings))