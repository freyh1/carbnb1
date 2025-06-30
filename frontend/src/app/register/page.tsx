"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/common/navbar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { fetchFromAPI, api } from "@/lib/api";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password1: "",
    password2: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (form.password1 !== form.password2) {
      setError("Passwords do not match");
      return;
    }
    try {
      await fetchFromAPI(api.auth.restAuth.registration, {
        method: "POST",
        body: JSON.stringify(form),
      });
      router.push("/login");
    } catch (err) {
      console.error(err);
      setError("Registration failed");
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
          <h1 className="text-2xl font-bold text-center">Create account</h1>
          <Input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            required
          />
          <Input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <Input
            name="password1"
            type="password"
            placeholder="Password"
            value={form.password1}
            onChange={handleChange}
            required
          />
          <Input
            name="password2"
            type="password"
            placeholder="Confirm password"
            value={form.password2}
            onChange={handleChange}
            required
          />
          {error && <p className="text-destructive text-sm">{error}</p>}
          <Button type="submit" className="w-full">
            Register
          </Button>
        </form>
      </main>
    </div>
  );
}
