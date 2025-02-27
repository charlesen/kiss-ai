from fastapi import Header, HTTPException, status

async def verify_api_key(x_api_key: str = Header(...)):
    # Par exemple, vérifiez la clé API avec une valeur dans la configuration ou dans une base de données
    if x_api_key != "votre_clé_attendue":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide."
        )
    return x_api_key
