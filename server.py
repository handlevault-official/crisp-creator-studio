# I-update ang init_db() para maglaman ng creator_blueprints table
def init_db():
    conn = sqlite3.connect("database.sqlite3")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_number TEXT UNIQUE NOT NULL,
            customer_email TEXT NOT NULL,
            product_id TEXT NOT NULL,
            payment_channel TEXT NOT NULL,
            license_key TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'verified',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            resume_data TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Bagong table para sa YouTube Creator Studio blueprints
    conn.execute("""
        CREATE TABLE IF NOT EXISTS creator_blueprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            channel_name TEXT,
            blueprint_data TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Pydantic model para sa Creator Blueprint
class CreatorBlueprintRequest(BaseModel):
    email: str
    channel_name: str
    blueprint_data: dict

@app.post("/api/creator/save")
def save_creator_blueprint(data: CreatorBlueprintRequest):
    """
    I-save o i-update ang YouTube blueprint sa SQLite database gamit ang email.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    import json
    data_str = json.dumps(data.blueprint_data)
    
    try:
        cursor.execute("""
            INSERT INTO creator_blueprints (email, channel_name, blueprint_data) 
            VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET 
            channel_name=excluded.channel_name, 
            blueprint_data=excluded.blueprint_data, 
            updated_at=CURRENT_TIMESTAMP
        """, (data.email, data.channel_name, data_str))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    
    conn.close()
    return {"success": True, "message": "Creator blueprint successfully saved to cloud!"}

@app.get("/api/creator/{email}")
def load_creator_blueprint(email: str):
    """
    Kunin ang nakaimbak na YouTube blueprint mula sa server gamit ang email.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT blueprint_data FROM creator_blueprints WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Walang nahanap na blueprint para sa email na ito.")
    
    import json
    return {"success": True, "blueprint_data": json.loads(row["blueprint_data"])}
