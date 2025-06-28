export interface Car {
    id: number;
    make: string;
    model: string;
    images: CarImage[];
    pricePerDay: number;
    isAvailable:boolean;
    location: Location;
  }
  
export interface CarImage {
  image: string;
}

export interface Location {
  city: string;
  country: string;
}