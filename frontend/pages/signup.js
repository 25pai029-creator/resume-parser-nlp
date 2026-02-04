import { useState } from "react";
import { supabase } from "../utils/supabase";
import { useRouter } from "next/router";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const signup = async () => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      /*alert(error.message);*/
       alert("Already signed up with this email id");
    } else {
      alert("Signup successful! Please login.");
      router.push("/login");
    }
  };

  return (
    <div className="center">
      <div className="card">
        <h2>Create Account</h2>

        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={signup}>Sign Up</button>
      </div>
    </div>
  );
}
