import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { userService } from '../api/userService'
import { jwtDecode } from 'jwt-decode'
import { authService } from '../api/auth'

interface User {
  id: string
  username: string
  email: string
}

interface AuthContextType {
  token: string | null
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<boolean>
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  register: (username: string, email: string, password: string) => Promise<void>
  fetchUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  // Verifica se o token está expirado
  const isTokenExpired = useCallback((token: string) => {
    try {
      const { exp } = jwtDecode(token)
      return Date.now() >= exp! * 1000
    } catch {
      return true
    }
  }, [])

  // Carrega o usuário e verifica autenticação
  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('token')

      if (!storedToken) {
        setIsLoading(false)
        return
      }

      if (isTokenExpired(storedToken)) {
        try {
          const refreshed = await refreshToken()
          if (!refreshed) {
            logout()
          }
        } catch {
          logout()
        }
      } else {
        setToken(storedToken)
        await fetchUser()
      }

      setIsLoading(false)
    }

    initializeAuth()
  }, [isTokenExpired])

  const fetchUser = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const userData = await userService.getMe() as User
      setUser(userData)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      setError('Failed to load user data')
      logout()
    } finally {
      setIsLoading(false)
    }
  }

  const refreshToken = async (): Promise<boolean> => {
    try {
      setIsLoading(true)
      setError(null)
      const newToken = await authService.refreshToken()

      if (!newToken || isTokenExpired(newToken)) {
        return false
      }

      setToken(newToken)
      localStorage.setItem('token', newToken)
      await fetchUser()
      return true
    } catch (error) {
      console.error('Failed to refresh token:', error)
      setError('Session expired. Please login again.')
      return false
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true)
      setError(null)
      const { token: newToken, user: userData } = await authService.login(email, password)

      if (!newToken || isTokenExpired(newToken)) {
        throw new Error('Invalid token received')
      }

      setToken(newToken)
      setUser(userData)
      localStorage.setItem('token', newToken)
      navigate('/')
    } catch (error) {
      console.error('Login failed:', error)
      setError('Invalid email or password')
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (username: string, email: string, password: string) => {
    try {
      setIsLoading(true)
      setError(null)
      await authService.register(username, email, password)
      await login(email, password)
    } catch (error) {
      console.error('Registration failed:', error)
      setError('Registration failed. Please try again.')
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = useCallback(() => {
    setToken(null)
    setUser(null)
    setError(null)
    localStorage.removeItem('token')
    navigate('/login')
  }, [navigate])

  // Limpa o estado de erro após 5 segundos
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000)
      return () => clearTimeout(timer)
    }
  }, [error])

  const value = {
    token,
    user,
    isAuthenticated: !!token && !isTokenExpired(token),
    isLoading,
    error,
    login,
    register,
    logout,
    refreshToken,
    fetchUser,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}