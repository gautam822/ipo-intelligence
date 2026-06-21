import { Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import Home from "./pages/Home"
import Listings from "./pages/Listings"
import TrackRecord from "./pages/TrackRecord"
import About from "./pages/About"

export default function App() {
  return (
    <div className="min-h-screen bg-bg text-ink font-sans">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/listings" element={<Listings />} />
        <Route path="/track-record" element={<TrackRecord />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  )
}
