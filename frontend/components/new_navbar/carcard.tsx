import { Card, CardContent, CardMedia, Typography, Button } from '@mui/material';
import { useRouter } from 'next/navigation';

interface CarCardProps {
  car: {
    id: number;
    make: string;
    model: string;
    year: number;
    price_per_day: number;
    seats: number;
    image: string;
  };
}

const CarCard = ({ car }: CarCardProps) => {
  const router = useRouter();

  const handleViewDetails = () => {
    // Navigate to a detailed page for the car (for example, /cars/1)
    router.push(`/cars/${car.id}`);
  };

  return (
    <Card sx={{ maxWidth: 345, margin: '1rem', boxShadow: 3 }}>
      <CardMedia
        component="img"
        height="140"
        image={car.image || 'car_silhoutte.png'}
        alt={`${car.make} ${car.model}`}
      />
      <CardContent>
        <Typography variant="h6">{`${car.make} ${car.model}`}</Typography>
        <Typography variant="body2" color="text.secondary">
          {`Year: ${car.year}`}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {`Seats: ${car.seats}`}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {`Price: $${car.price_per_day} per day`}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          sx={{ marginTop: '1rem' }}
          onClick={handleViewDetails}
        >
          View Details
        </Button>
      </CardContent>
    </Card>
  );
};

export default CarCard;
