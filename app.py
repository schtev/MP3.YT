import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");
  const [bitrate, setBitrate] = useState("192");
  const [queue, setQueue] = useState([]);

  const addToQueue = () => {
    if (!url) return;
    setQueue([
      ...queue,
      { url, status: "pending", title: "Loading...", thumbnail: null }
    ]);
    fetchMeta(url, queue.length);
    setUrl("");
  };

  const fetchMeta = async (url, index) => {
    const res = await fetch(`https://noembed.com/embed?url=${url}`);
    const data = await res.json();

    setQueue(prev => {
      const updated = [...prev];
      updated[index].title = data.title;
      updated[index].thumbnail = data.thumbnail_url;
      return updated;
    });
  };

  const downloadItem = async (item, index) => {
    updateStatus(index, "downloading");

    const res = await fetch("https://YOUR-RENDER-URL.onrender.com/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: item.url, bitrate })
    });

    const blob = await res.blob();
    const audioUrl = URL.createObjectURL(blob);

    updateStatus(index, "done", audioUrl);
  };

  const updateStatus = (index, status, audio=null) => {
    setQueue(prev => {
      const updated = [...prev];
      updated[index].status = status;
      if (audio) updated[index].audio = audio;
      return updated;
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-xl mx-auto bg-white rounded-2xl shadow p-4">
        <h1 className="text-2xl font-bold text-center mb-4">YT → MP3</h1>

        <input
          className="w-full p-3 border rounded mb-2"
          placeholder="Paste YouTube URL"
          value={url}
          onChange={(e)=>setUrl(e.target.value)}
        />

        <div className="flex gap-2 mb-3">
          <select
            className="flex-1 p-2 border rounded"
            value={bitrate}
            onChange={(e)=>setBitrate(e.target.value)}
          >
            <option value="128">128</option>
            <option value="192">192</option>
            <option value="256">256</option>
            <option value="320">320</option>
          </select>

          <button
            className="bg-blue-600 text-white px-4 rounded"
            onClick={addToQueue}
          >Add</button>
        </div>

        {queue.map((item,i)=> (
          <div key={i} className="border p-2 rounded mb-3">
            {item.thumbnail && (
              <img src={item.thumbnail} className="w-full rounded mb-2" />
            )}

            <div className="font-semibold text-sm">{item.title}</div>
            <div className="text-xs">{item.status}</div>

            {item.audio && (
              <audio controls className="w-full mt-2">
                <source src={item.audio} type="audio/mpeg" />
              </audio>
            )}

            {item.status === "pending" && (
              <button
