import { useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from '../components/common/Navbar'
import Footer from '../components/common/Footer'
import { APP_NAME } from '../utils/constants'

function MainLayout() {
  useEffect(() => {
    document.title = APP_NAME
  }, [])

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}

export default MainLayout
