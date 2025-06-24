"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Navbar from "@/components/common/navbar";
import CarCard from "@/components/common/car-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getCars } from "@/lib/api";
import { Car } from "@/types/car";

export default function Home() {
  const [cars, setCars] = useState<Car[]>([]);

  useEffect(() => {
    getCars()
      .then(setCars)
      .catch((err) => console.error("Failed to fetch cars:", err));
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <section className="relative h-[60vh] flex items-center justify-center">
          <Image
            src="https://images.unsplash.com/photo-1503376780353-7e6692767b70"
            alt="Car background"
            fill
            priority
            className="object-cover"
          />
          <div className="absolute inset-0 bg-black/40" />
          <div className="relative z-10 text-center text-background max-w-xl px-4">
            <h1 className="text-4xl font-bold mb-4">Find your perfect ride</h1>
            <p className="mb-6 text-lg">
              Book unique cars from local hosts around the world.
            </p>
            <form className="bg-white/80 dark:bg-black/50 backdrop-blur-sm rounded-lg p-4 flex flex-col sm:flex-row gap-2">
              <Input placeholder="Pickup location" className="flex-1" />
              <Input type="date" className="sm:max-w-[160px]" />
              <Input type="date" className="sm:max-w-[160px]" />
              <Button type="submit">Search</Button>
            </form>
          </div>
        </section>

        <section className="py-12 px-4 max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold mb-6">Featured Cars</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {cars.map((car) => (
              <CarCard
                key={car.id}
                car={{
                  id: car.id,
                  title: `${car.make} ${car.model}`,
                  location: `${car.location?.city}, ${car.location?.country}`,
                  price: `$${car.price_per_day}/night`,
                  image: car.images[0]?.image || "/placeholder.jpg",
                }}
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
