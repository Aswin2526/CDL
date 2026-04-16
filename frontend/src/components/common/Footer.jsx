import { APP_NAME } from '../../utils/constants'

function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white py-6 text-center text-sm text-gray-500">
      <p>
        &copy; {new Date().getFullYear()} {APP_NAME} — Online Painting Gallery & Store
      </p>
    </footer>
  )
}

export default Footer
