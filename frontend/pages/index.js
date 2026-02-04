import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();

  return (
    <div className="center">
      <div className="card">
        <h1>Resume Parser – HR Portal</h1>

        <button onClick={() => router.push("/signup")}>
          Sign Up
        </button>

        <button className="outline" onClick={() => router.push("/login")}>
          Login
        </button>
      </div>
    </div>
  );
}
  /*
import { useState } from "react";
import { supabase } from "../utils/supabase";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (!error) window.location.href = "/dashboard";
    else alert(error.message);
  };

  const signup = async () => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (!error) alert("Signup successful, now login");
    else alert(error.message);
  };

  return (
    <div className="card">
      <h2>Login</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={login}>Login</button>
      <button onClick={signup}>Signup</button>
    </div>
  );
}
*/