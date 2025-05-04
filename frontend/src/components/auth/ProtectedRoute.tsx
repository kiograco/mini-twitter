import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export function ProtectedRoute() {
  const { isAuthenticated } = useAuth()

  console.log('ProtectedRoute', isAuthenticated)

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />
}