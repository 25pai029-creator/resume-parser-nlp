import { useState } from "react";

export default function Upload() {
  const [job, setJob] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = async () => {
    if (!file || !job) {
      alert("Please enter job description and select resume file");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const form = new FormData();
      form.append("resume", file);
      form.append("job_description", job);

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/parse`,
        {
          method: "POST",
          body: form,
        }
      );

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Backend not responding. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Resume Analyzer</h2>

      <textarea
        placeholder="Enter Job Description"
        value={job}
        onChange={(e) => setJob(e.target.value)}
      />

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div className="result">
          <p><b>Match Score:</b> {result.match_score}</p>
          <p><b>Roles:</b> {result.roles?.join(", ")}</p>
          <p><b>Experience:</b> {result.experience?.join(", ")}</p>
        </div>
      )}
    </div>
  );
}
