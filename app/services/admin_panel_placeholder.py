# Admin panel için temel yapı placeholder'ı
def list_uploaded_cases(directory="uploaded_videos"):
    import os
    return [f for f in os.listdir(directory) if f.endswith(".avi")]
