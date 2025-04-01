import os
import urllib.request

def download_landmark_predictor():
    """Download Dlib's 68-point facial landmark predictor."""
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    local_filename = "shape_predictor_68_face_landmarks.dat.bz2"
    extracted_filename = "shape_predictor_68_face_landmarks.dat"

    # Check if file already exists
    if os.path.exists(extracted_filename):
        print(f"✅ {extracted_filename} already exists.")
        return

    try:
        # Download the file
        print("⬇️ Downloading facial landmark predictor...")
        urllib.request.urlretrieve(url, local_filename)

        # Extract the file (requires bzip2)
        import bz2
        with bz2.open(local_filename, 'rb') as source:
            with open(extracted_filename, 'wb') as target:
                target.write(source.read())

        # Remove compressed file
        os.remove(local_filename)

        print(f"✅ Successfully downloaded {extracted_filename}")

    except Exception as e:
        print(f"❌ Error downloading landmark predictor: {e}")

if __name__ == "__main__":
    download_landmark_predictor()
