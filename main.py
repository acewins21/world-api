from fastapi import FastAPI, UploadFile, File
import re

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Shadow API Scanner", "status": "operational"}

@app.post("/scan")
async def scan_logs(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode()
    
    apis = []
    for line in text.split('\n'):
        if 'GET' in line or 'POST' in line:
            match = re.search(r'(GET|POST|PUT|DELETE)\s+(/[^\s]+)', line)
            if match:
                method, path = match.groups()
                risk = "CRITICAL" if '/admin' in path or '/internal' in path else "MEDIUM"
                apis.append({"method": method, "path": path, "risk": risk})
    
    return {
        "shadow_apis_found": len(apis),
        "critical_count": sum(1 for a in apis if a['risk'] == "CRITICAL"),
        "apis": apis
    }
