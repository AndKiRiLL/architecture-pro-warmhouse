@app.get("/health")
async def health_check():
    """Health check endpoint for k8s/docker"""
    db_healthy = await db.health_check()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "service": "device-service"
    }