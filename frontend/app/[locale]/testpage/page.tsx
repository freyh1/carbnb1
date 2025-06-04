'use client';

import CarCard from '@/components/new_navbar/carcard'; 
import { Car } from '@/types/types';
import { Box, Stack } from '@mui/material';
import { useEffect, useState } from "react";


export default function TestPage() {
  const [cars, setCars] = useState<Car[]>([]);

  useEffect(() => {
    async function fetchCars() {
      try {
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
        const response = await fetch(`${API_BASE_URL}/cars`);
        const data = await response.json();
        console.log("The datatype is: ", typeof data)
        console.log("The datatype is: ", Object.keys(data))
        setCars(data);
      } catch (error) {
        console.error("Error fetching cars: ", error);
      }
    }

    fetchCars();
  }, []);

  return (
    <Box display="flex" justifyContent="center" p={4}>
      <Stack spacing={4}>
        {cars.map((car) => (
          <CarCard key={car.id} car={car} />
        ))}
      </Stack>
    </Box>
  );
}
