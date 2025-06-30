"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/common/navbar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { fetchFromAPI, api } from "@/lib/api";

export default function CreateCarPage() {
  const [form, setForm] = useState({
    make: "",
    model: "",
    price_per_day: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await fetchFromAPI(api.cars.base, {
        method: "POST",
        body: JSON.stringify({
          make: form.make,
          model: form.model,
          price_per_day: parseFloat(form.price_per_day),
        }),
      });
      router.push("/my-cars");
    } catch (err) {
      console.error(err);
      setError("Failed to create car");
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
          <h1 className="text-2xl font-bold text-center">Register your car</h1>
          <Input
            name="make"
            placeholder="Make"
            value={form.make}
            onChange={handleChange}
            required
          />
          <Input
            name="model"
            placeholder="Model"
            value={form.model}
            onChange={handleChange}
            required
          />
          <Input
            name="price_per_day"
            type="number"
            step="0.01"
            placeholder="Price per day"
            value={form.price_per_day}
            onChange={handleChange}
            required
          />
          {error && <p className="text-destructive text-sm">{error}</p>}
          <Button type="submit" className="w-full">
            Save
          </Button>
        </form>
      </main>
    </div>
  );
}
