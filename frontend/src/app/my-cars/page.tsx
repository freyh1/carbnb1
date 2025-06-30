"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/common/navbar";
import { fetchFromAPI, api } from "@/lib/api";
import { Car } from "@/types/car";
import CarCard from "@/components/common/car-card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function MyCarsPage() {
  const [cars, setCars] = useState<Car[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchFromAPI<Car[]>(api.cars.mine)
      .then(setCars)
      .catch(() => setError("Failed to load cars"));
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 px-4 py-8 max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Your Cars</h1>
          <Button asChild>
            <Link href="/create-car">Add listing</Link>
          </Button>
        </div>
        {error && <p className="text-destructive mb-4">{error}</p>}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {cars.map((car) => (
            <CarCard key={car.id} car={car} />
          ))}
        </div>
      </main>
    </div>
  );
}
