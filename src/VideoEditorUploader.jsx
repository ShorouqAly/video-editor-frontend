import { React, useState } from "react";
import axios from "axios";

export default function VideoEditorUploader() {
  const [videos, setVideos] = useState([]);
  const [photos, setPhotos] = useState([]);
  const [music, setMusic] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleUpload = async () => {
    setLoading(true);
    setDownloadUrl(null);

    const formData = new FormData();
    videos.forEach((file) => formData.append("videos", file));
    photos.forEach((file) => formData.append("photos", file));
    if (music) formData.append("music", music);

    try {
      const response = await axios.post("https://YOUR-BACKEND-URL/create-video/", formData, {
        responseType: "blob",
        headers: { "Content-Type": "multipart/form-data" },
      });

      const blob = new Blob([response.data], { type: "video/mp4" });
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Family Video Summary</h1>

      <div className="mb-4">
        <label className="block mb-1">Upload Videos</label>
        <input type="file" multiple accept="video/*" onChange={(e) => setVideos(Array.from(e.target.files))} />
      </div>

      <div className="mb-4">
        <label className="block mb-1">Upload Photos</label>
        <input type="file" multiple accept="image/*" onChange={(e) => setPhotos(Array.from(e.target.files))} />
      </div>

      <div className="mb-4">
        <label className="block mb-1">Optional Music</label>
        <input type="file" accept="audio/*" onChange={(e) => setMusic(e.target.files[0])} />
      </div>

      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
        {loading ? "Creating..." : "Create Video"}
      </button>

      {downloadUrl && (
        <div className="mt-6">
          <a href={downloadUrl} download="family_summary.mp4" className="text-blue-600 underline">
            Download Final Video
          </a>
        </div>
      )}
    </div>
  );
}
