import Image from "next/image"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"

export interface Car {
  id: number
  title: string
  location: string
  price: string
  image: string
}

export default function CarCard({ car }: { car: Car }) {
  return (
    <Card className="overflow-hidden">
      <Image
        src={car.image}
        alt={car.title}
        width={400}
        height={300}
        className="h-48 w-full object-cover"
      />
      <CardHeader className="pb-2">
        <CardTitle className="text-base">{car.title}</CardTitle>
        <CardDescription>{car.location}</CardDescription>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="font-medium">{car.price}</p>
      </CardContent>
    </Card>
  )
}