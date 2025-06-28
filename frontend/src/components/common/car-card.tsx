import Image from "next/image"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"
import { Car } from "@/types/car"

export default function CarCard({ car }: { car: Car }) {
  return (
    <Card className="overflow-hidden">
      <Image
        src={car.images[0].image}
        alt={car.make}
        width={400}
        height={300}
        className="h-48 w-full object-cover"
      />
      <CardHeader className="pb-2">
        <CardTitle className="text-base">{car.make}</CardTitle>
        <CardDescription>{car.location.city}</CardDescription>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="font-medium">{car.pricePerDay}</p>
      </CardContent>
    </Card>
  )
}