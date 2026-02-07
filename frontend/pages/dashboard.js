import { useState } from "react";
import { supabase } from "../utils/supabase";

export default function Dashboard() {
  const [activeMenu, setActiveMenu] = useState("home");
  const [jobDesc, setJobDesc] = useState("");
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const analyze = async () => {
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);

   /* const res = await fetch("http://127.0.0.1:8000/parse", {
      method: "POST",
      body: formData,
    });*/
     const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/parse`,
        {
          method: "POST",
          body: form,
        }
      );
    const data = await res.json();
    setResult(data);
  };

  const logout = async () => {
    await supabase.auth.signOut();
    window.location.href = "/";
  };

  return (
    <div className="dashboard">

      {/* 🔹 TOP BAR */}
      <div className="topbar">
        <button
          className="menu-btn"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          ☰
        </button>
        <h3>HR Dashboard</h3>
      </div>

      {/* 🔹 SIDEBAR */}
      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <h3>HR Panel</h3>

        <button
          onClick={() => {
            setActiveMenu("analyze");
            setSidebarOpen(false);
          }}
        >
          Analyze Resume
        </button>

        <button className="logout" onClick={logout}>
          Logout
        </button>
      </div>

      {/* 🔹 MAIN CONTENT */}
      <div className="content">
        {activeMenu === "home" && (
          <h2>Welcome to HR Dashboard</h2>
        )}

        {activeMenu === "analyze" && (
          <div className="card1">
            <h2>Resume Analyzer</h2>

            <textarea
              placeholder="Enter Job Description"
              onChange={(e) => setJobDesc(e.target.value)}
            />

            <input
              type="file"
              onChange={(e) => setResume(e.target.files[0])}
            />

            <button onClick={analyze}>Analyze</button>

            {result && (
              <div className="result">
                <p><b>Match Score:</b> {result.match_score}%</p>
                <p><b>Decision:</b> {result.hiring_decision}</p>

                <p><b>Matched Skills:</b></p>
                <ul>
                  {result.matched_skills.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>

                <p><b>Missing Skills:</b></p>
                <ul>
                  {result.missing_skills.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>

                <p><b>Detected Roles:</b></p>
                <ul>
                  {result.extracted_roles.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>

                <p><b>Experience:</b></p>
                <ul>
                  {result.experience.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
