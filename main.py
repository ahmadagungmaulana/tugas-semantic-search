import json
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Inisialisasi Aplikasi FastAPI
app = FastAPI(title="Genshin Impact Semantic Search API")

# Load Model Embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Inisialisasi Qdrant Vector Database (In-Memory)
qdrant = QdrantClient(":memory:")
COLLECTION_NAME = "genshin_characters"

@app.on_event("startup")
def startup_db():
    # Buat Collection di Qdrant
    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    # Read dataset.json
    with open("dataset.json", "r", encoding="utf-8") as f:
        characters = json.load(f)
    
    # Generasi Vektor & Simpan ke Qdrant
    points = []
    for idx, char in enumerate(characters, start=1):
        # Penggabungan teks standar dan sederhana sesuai tutorial
        text_content = (
            f"Character: {char['character_name']}, "
            f"Rarity: {char['star_rarity']} star, "
            f"Region: {char['region']}, "
            f"Vision: {char['vision']}, "
            f"Weapon: {char['weapon_type']}, "
            f"Affiliation: {char['affiliation']}, "
            f"Special Dish: {char['special_dish']}"
        )
        
        # Ubah teks menjadi vector embedding
        vector = model.encode(text_content).tolist()
        
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload=char
            )
        )
    
    # Masukkan data ke collection
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

# Schema Request
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

# Endpoint Pencarian (Semantic Search)
@app.post("/search")
def search_lore(req: SearchRequest):
    # Encodes query dari user menjadi vektor
    query_vector = model.encode(req.query).tolist()
    
    # Cari vektor terdekat di database Qdrant
    try:
        search_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=req.top_k
        )
    except Exception:
        response = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=req.top_k
        )
        search_results = response.points
    
    # Format response output
    results = []
    for hit in search_results:
        results.append({
            "score": round(hit.score, 4),
            "payload": hit.payload
        })
        
    return {
        "status": "success",
        "query": req.query,
        "results": results
    }   