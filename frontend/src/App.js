import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from "recharts";
 
function App() {
  const [sepalWidth, setSepalWidth] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
 
  const handlePredict = async (e) => {
    e.preventDefault();
    setError(null);
    setPrediction(null);
    setLoading(true);
 
    try {
      const res = await fetch("http://localhost:3031/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sepal_width: parseFloat(sepalWidth) }),
      });
 
      const data = await res.json();
      if (res.ok) {
        setPrediction(data.prediction);
      } else {
        setError(data.error || "Erreur serveur");
      }
    } catch {
      console.log(error)
      setError("❌ Serveur injoignable.");
    } finally {
      setLoading(false);
    }
  };
 
  const avgSepalLength = 5.8;
 
  const graphData = [
    { name: "Valeur prédite", value: prediction, fill: "#198754" },
    { name: "Moyenne du dataset", value: avgSepalLength, fill: "#0d6efd" },
  ];
 
  return (
    <div style={styles.page}>
      <div style={styles.background}></div>
      <div style={styles.card}>
        <h1 style={styles.title}>🌸 Prédire la longueur de sépale</h1>
 
        <form onSubmit={handlePredict} style={styles.form}>
          <input
            type="number"
            step="0.01"
            placeholder="Largeur de sépale (cm)"
            value={sepalWidth}
            onChange={(e) => setSepalWidth(e.target.value)}
            required
            style={styles.input}
          />
          <button
            type="submit"
            style={{ ...styles.button, opacity: loading ? 0.6 : 1 }}
            disabled={loading}
          >
            {loading ? "Prédiction..." : "Prédire"}
          </button>
        </form>
 
        {prediction !== null && (
          <>
            <div style={styles.prediction}>
              📏 Longueur prédite : <strong>{prediction} cm</strong>
            </div>
 
            <div style={{ width: "100%", height: 200, marginTop: 30 }}>
              <ResponsiveContainer>
                <BarChart layout="vertical" data={graphData}>
                  <XAxis type="number" domain={[4, 8]} />
                  <YAxis type="category" dataKey="name" />
                  <Tooltip />
                  <Bar dataKey="value">
                    <LabelList dataKey="value" position="right" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
 
        {error && <div style={styles.error}>{error}</div>}
      </div>
    </div>
  );
}
 
const styles = {
  page: {
    position: "relative",
    fontFamily: "Inter, sans-serif",
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "1rem",
    overflow: "hidden",
  },
  background: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundImage: `url("/Wallpaper Check Board.jpeg")`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    filter: "blur(6px)",
    zIndex: 0,
  },
  card: {
    position: "relative",
    zIndex: 1,
    background: "#f1f3f6",
    padding: "2rem",
    borderRadius: "16px",
    boxShadow: "10px 10px 20px #d1d9e6, -10px -10px 20px #ffffff",
    width: "100%",
    maxWidth: "500px",
    textAlign: "center",
  },
  title: {
    marginBottom: "1.5rem",
    fontSize: "1.6rem",
    color: "#333",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  input: {
    padding: "0.75rem",
    borderRadius: "12px",
    border: "1px solid #ccc",
    fontSize: "1rem",
    outline: "none",
  },
  button: {
    padding: "0.75rem",
    fontSize: "1rem",
    borderRadius: "12px",
    backgroundColor: "#0d6efd",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    transition: "background 0.3s ease",
  },
  prediction: {
    marginTop: "1.5rem",
    fontSize: "1.25rem",
    color: "#198754",
  },
  error: {
    marginTop: "1rem",
    color: "#dc3545",
    fontWeight: "500",
  },
};
 
export default App;