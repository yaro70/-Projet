import React from 'react';
import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children, requirePatron = false, requireCollaborateur = false }) {
  const token = localStorage.getItem('token');
  const isPatron = localStorage.getItem('is_patron') === 'true';
  const isCollaborateur = localStorage.getItem('is_collaborateur') === 'true';

  // Rediriger si non connecté
  if (!token) {
    return <Navigate to="/login" />;
  }

  // Rediriger si le rôle ne correspond pas
  if (requirePatron && !isPatron) {
    return <Navigate to="/login" />;
  }

  if (requireCollaborateur && !isCollaborateur) {
    return <Navigate to="/login" />;
  }

  // Sinon, afficher la route protégée
  return children;
}
