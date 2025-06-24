import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"

export default function Navbar() {
  return (
    <header className="border-b bg-background sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4 px-4 py-3">
        <Link href="/" className="text-lg font-bold">
          carbnb
        </Link>
        <div className="flex-1 max-w-md">
          <Input placeholder="Search cars" />
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost">Login</Button>
          <Button>Sign up</Button>
        </div>
      </div>
    </header>
  )
}