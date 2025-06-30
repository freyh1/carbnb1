"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/common/navbar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { fetchFromAPI, api } from "@/lib/api";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await fetchFromAPI(api.auth.login, {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      router.push("/");
    } catch (err) {
      console.error(err);
      setError("Invalid credentials");
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 flex items-center justify-center px-4">
        <form
          onSubmit={handleSubmit}
          className="bg-white/80 dark:bg-black/50 backdrop-blur-sm rounded-lg p-6 w-full max-w-sm space-y-4"
        >
          <h1 className="text-2xl font-bold text-center">Login</h1>
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="text-destructive text-sm">{error}</p>}
          <Button type="submit" className="w-full">
            Login
          </Button>
        </form>
      </main>
    </div>
  );
}
