import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';

import Commande from './components/Commande';
import Login from './components/Login';
import DashboardPatron from './components/DashboardPatron';
import DashboardCollaborateur from './components/DashboardCollaborateur';
import Evenements from './components/Evenements';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './components/Home';



export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/commander/:gateauId" element={<Commande />} />
          <Route path="/login" element={<Login />} />
          <Route path="/patron/dashboard" element={
    <ProtectedRoute requirePatron={true}>
      <DashboardPatron />
    </ProtectedRoute>
  } />

  <Route path="/collaborateur/dashboard" element={
    <ProtectedRoute requireCollaborateur={true}>
      <DashboardCollaborateur />
    </ProtectedRoute>
  } />

          <Route path="/evenements" element={<Evenements />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}