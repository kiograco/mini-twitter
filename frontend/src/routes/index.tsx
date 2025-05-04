import { lazy } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from '../components/auth/ProtectedRoute'
import { AuthProvider } from '../context/AuthContext'

// const Profile = lazy(() => import('@/pages/Profile'))
// const PostDetail = lazy(() => import('@/pages/PostDetail'))
const Login = lazy(() => import('../pages/Login'))
const Register = lazy(() => import('../pages/Register'))
const Feed = lazy(() => import('../pages/Feed'))


export const AppRoutes = () => {
  return (
    <AuthProvider>
      <Routes>
        <Route path="*" element={<Navigate to='/login' />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Feed />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}