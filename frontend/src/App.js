import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");
  const [bitrate, setBitrate] = useState("192");
  const [queue, setQueue] = useState([]);

  const addToQueue = () => {
    if (!url) return;

    setQueue([
      ...queue,
      {
        url,
        status: "pending",
        title: "Loading...",
        thumbnail: null,
      },
    ]);

    fetchMeta(url, queue.length);
    setUrl("");
  };

  const fetchMeta = async (url, index) => {
    try {
      const res = await fetch(`https://noembed.com/embed?url=${url}`);
      const data = await res.json();

      setQueue((prev) => {
        const updated = [...prev];
        updated[index].title = data.title;
        updated[index].thumbnail = data.thumbnail_url;
        return updated;
      });
    } catch (e) {
      console.error(e);
    }
  };

  const downloadItem = async (item, index) => {
    updateStatus(index, "downloading");

    const res = await fetch("https://YOUR-RENDER-URL.onrender.com/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: item.url, bitrate }),
    });

    const blob = await res.blob();
    const audioUrl = URL.createObjectURL(blob);

    updateStatus(index, "done", audioUrl);
  };

  const updateStatus = (index, status, audio = null) => {
    setQueue((prev) => {
      const updated = [...prev];
      updated[index].status = status;
      if (audio) updated[index].audio = audio;
      return updated;
    });
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>YT → MP3</h1>

      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste YouTube URL"
      />

      <select
        value={bitrate}
        onChange={(e) => setBitrate(e.target.value)}
      >
        <option value="128">128</option>
        <option value="192">192</option>
        <option value="256">256</option>
        <option value="320">320</option>
      </select>

      <button onClick={addToQueue}>Add</button>

      {queue.map((item, i) => (
        <div key={i}>
          <p>{item.title}</p>
          <p>{item.status}</p>

          {item.audio && (
            <audio controls src={item.audio}></audio>
          )}

          {item.status === "pending" && (
            <button onClick={() => downloadItem(item, i)}>
              Download
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
